### Web Scraping with Phantomjs

Install phantomjs on your machine then run any of the `.js` file below using the command: `phantomjs filename.js` in the command line


### Using phantomjs to scrape data from facebook

#### Current functionality 

* `facebook_scrape.js` will grab the html content from facebook containing your top 20 friends. I'm trying to figure out how to use phantomjs to scroll (and fully load the page afterwards) so that more friends names can be added
* `get_friends_from_html.py` uses beautiful soup to extract the friends names from the html

#### To do

* I want to extract all friend names. Then use the names to go back to facebook and pull friend information such as location 
* Ultimately the goal being to be able to sort friends alphabetically, and search through friends by location (the functionality that once existed on facebook)

### Using phantomjs to scrape retail fx quotes from different sources

* torfx_scrape.js