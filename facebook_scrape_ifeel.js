// facebook_scrape.js

// login to facebook code is from here:
// https://gist.github.com/ecin/2473860
// https://github.com/manishjo/Automation/blob/master/facebook_automation/fbScreenshot.js

var page = require('webpage').create();
var fs = require('fs');
var fb_password = fs.read('facebook_credentials.txt')

function mouseClick(element) {
	// create a mouse click event
	var event = document.createEvent('MouseEvents');
	event.initMouseEvent('click', true, true, window, 1, 0, 0);

	// send click to element
	element.dispatchEvent(event);
}

var fillLoginInfo = function(password){
  	var frm = document.getElementById("login_form");
    frm.elements["email"].value = 'robert.david.west@gmail.com';
    frm.elements["pass"].value = password;
    frm.submit();
}

var i = 0
page.onLoadFinished = function(){

	console.log('Page Title: ' + page.title)
	console.log('iterator: ' + i)

	if(i==0){
		page.evaluate(fillLoginInfo, fb_password);
		i++;
	}
	else {
		page.render('screenshot_feel.png');
		//fs.write('friends.html', page.content, 'w');
		console.log("completed");
		phantom.exit();		
	}
}
page.open('https://www.facebook.com/events/1484325528528581/')