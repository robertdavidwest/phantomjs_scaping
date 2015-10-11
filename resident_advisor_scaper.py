import requests
import cookielib
from requests import session
import re
import urllib2

event_url = 'http://www.residentadvisor.net/event.aspx?'
event_id = '754573'  # cityfox_halloween_
cityfox_halloween = 'http://www.residentadvisor.net/event.aspx?754573'

jar = cookielib.CookieJar()
login_url = 'https://www.residentadvisor.net/login'

acc_pwd = {'UsernameOrEmailAddress':'rwba15181@gmail.com',
           'Password':'SOMEPASSWORD',
           'StayLoggedIn':'true',
           'StayLoggedIn':'false'
}

r = requests.get(login_url, cookies=jar)
r = requests.post(login_url, cookies=jar, data=acc_pwd)

response = urllib2.urlopen(event_url+event_id)
html = response.read()
num_str = html[html.find('tickettypes'):html.find('data-shiptype')]
ticketId = re.findall(r'\d+', num_str)[0]

print ticketId

ticket_url = 'http://www.residentadvisor.net/Output/baskethandler.ashx'
acc_ticket = {'type': 'addBasket',
              'ticketId': str(ticketId),
              'shippingTypeId': '8',
              'quantity':'1',
              'eventId': event_id,
              'currencyId': '4',
              'referrer': 'http://www.residentadvisor.net/events.aspx'
}

#ticket_url2 = 'http://www.residentadvisor.net/event.aspx?664410'
#r = requests.get(ticket_url2, cookies=jar)
r = requests.post(ticket_url, cookies=jar, data=acc_ticket)
print r
print r.content
import ipdb; ipdb.set_trace()

with session() as c:
    c.post(login_url, data=acc_pwd)
    response = c.post(ticket_url, data=acc_ticket)
    print response.headers
    print response.text
