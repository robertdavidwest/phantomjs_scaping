
### Using phantomjs to scrape data from facebook

#### Current functionality 

* `facebook_scrape.js` will grab the html content from facebook containing your top 20 friends. I'm trying to figure out how to use phantomjs to scroll so that more friends names will be added
* `get_friends_from_html.py` uses beautiful soup extract the friends names from the html

#### To do

* I want extract all friends names. Then use the names to go back to facebook and pull friend information such as location 
* Ultimately the goal being to be able to sort friends alphabetically, and find friends in certain locations (the functionality that use to exist on facebook)