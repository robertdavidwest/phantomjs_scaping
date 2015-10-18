
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import os 
import time

# helper functions

def display_all_ids(driver, wait):
    all = wait.until(lambda driver: driver.find_elements_by_xpath("//*[@id]"))
    atts = []
    for a in all:
        atts.append(a.get_attribute("id"))
    atts.sort()
    for a in atts:
        print a

from asprise_ocr_api import Ocr, OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PLAINTEXT
def get_page_text(image_filename):     

    Ocr.set_up() # one time setup
    ocrEngine = Ocr()
    ocrEngine.start_engine("eng")
    s = ocrEngine.recognize(image_filename, -1, -1, -1, -1, -1,
                      OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PLAINTEXT)

    # recognizes more images here ..
    ocrEngine.stop_engine()

    return s


def get_kindle_text(driver_type, book_title, first_page, last_page):
    if driver_type == 'chrome':
        path_to_chromedriver = '/Users/rwest/Downloads/chromedriver' # change path as needed
        driver = webdriver.Chrome(executable_path=path_to_chromedriver)
    elif driver_type == 'phantomjs':
        # phantom js settings
        dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/45.0.2454.99")

        #path_to_phantomjs = '/Users/rwest/Desktop/phantomjs' # change path as needed
        path_to_phantomjs = 'phantomjs'
        driver = webdriver.PhantomJS(executable_path=path_to_phantomjs,
                                     desired_capabilities=dcap)


    url = 'https://www.amazon.com/ap/signin?openid.assoc_handle=amzn_kweb&openid.'\
          'return_to=https%3A%2F%2Fread.amazon.com%2F&openid.mode='\
          'checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.'\
          'net%2Fauth%2F2.0&openid.identity=http%3A%2F%2Fspecs.openid.'\
          'net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id='\
          'http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&'\
          'pageId=amzn_kcr'
    driver.get(url)

    # Fill out login form and submit
    email = driver.find_element_by_id("ap_email")
    password = driver.find_element_by_id("ap_password")
    email.send_keys("robert.david.west@gmail.com")
    with open('kindle_credentials.txt', 'rb') as file:
        password_str = file.read()
    password.send_keys(password_str)
    driver.find_element_by_id("signInSubmit-input").click()

    # Wait until logged in then switch to KindleLibraryIFrame
    wait = ui.WebDriverWait(driver, 10)
    iFrame = wait.until(lambda driver: driver.find_element_by_id('KindleLibraryIFrame'))
    driver.switch_to.frame(iFrame)

    # close pop up message to use offline reader
    driver.find_element_by_id('kindle_dialog_firstRun_button').click()

    # select chosen book
    books = wait.until(lambda driver: driver.find_elements_by_class_name('book_title'))
    #books = driver.find_elements_by_class_name('book_title')
    for book in books:
        print book.text
        if book.text == book_title:
            book.click()

    # wait until book opened then switch to KindleReaderIFrame
    driver.switch_to.default_content()
    iFrame2 = wait.until(lambda driver: driver.find_element_by_id('KindleReaderIFrame'))
    driver.switch_to.frame(iFrame2)

    # select first page of book
    page_number = '2'
    def copy_page(page_number):
        page_selector = wait.until(lambda driver: driver.find_element_by_id('kindleReader_button_goto'))
        wait.until(lambda driver: driver.find_element_by_id('kindleReader_button_goto'))

        hover = ActionChains(driver).move_to_element(page_selector) # make button visible

        condition = ''
        while (condition == ''):
            try:
                page_selector.click()
            except ElementNotVisibleException:
                hover = ActionChains(driver).move_to_element(page_selector) # make button visible
            else:
                condition = 'passed'

        condition = ''
        while (condition == ''):
            try:
                driver.find_element_by_id('kindleReader_goToMenuItem_goToLocation').click()
            except NoSuchElementException:
                page_selector.click()
            else:
                condition = 'passed'

        enter_page_num = wait.until(lambda driver: driver.find_element_by_id("kindleReader_dialog_gotoField"))
        enter_page_num.send_keys(page_number)
        buttons = driver.find_elements_by_class_name("ui-button")
        for b in buttons:
            if b.text == 'Go to location':
                b.click()

        time.sleep(7)
        driver.get_screenshot_as_file('temp.png')
        text = get_page_text('temp.png')
        os.remove('temp.png')
        
        return text

    results = []
    for i in xrange(first_page, last_page+1):
        text = copy_page(page_number=str(i))
        results.append(text)

    print results

    # use this code to change page
    '''
    arrow_buttons = driver.get_elements_by_class_name('kindleReader_arrowBtn')
    for ab in arrow_buttons:
        if ab.title == 'Next Page'
            hover = ActionChains(driver).move_to_element(ab) # make button visible
            ab.click()
    '''



### This is not working for phantomjs yet - only for chrome
driver_type = 'chrome'
book_title = 'Eastern Body, Western Mind: Psychology and the Chakra System As a Path to the Self'
first_page_num = 6373
last_page_num = 6374
get_kindle_text(driver_type, book_title, first_page=first_page_num, last_page=last_page_num)



