// facebook_scrape.js

// login to facebook code is from here:
// https://gist.github.com/ecin/2473860
// https://github.com/manishjo/Automation/blob/master/facebook_automation/fbScreenshot.js

var page = require('webpage').create();
var fs = require('fs');
var fx_password = fs.read('tor_credentials.txt')

function mouseClick(element) {
	// create a mouse click event
	var event = document.createEvent('MouseEvents');
	event.initMouseEvent('click', true, true, window, 1, 0, 0);

	// send click to element
	element.dispatchEvent(event);
}

var fillLoginInfo = function (password){
  	var frm = document.getElementById("loginPage");
    frm.elements["login_userName_input"].value = 'rwest@tepper.cmu.edu';
    frm.elements["login_password_input"].value = password;
    frm.submit();
}

var logout = function (mouseClick_fn){
	logout = document.getElementById('logoutID');
	//if (logout){
	mouseClick_fn(logout);
	//}
}

var get_rate = function (user_sell_amt, user_sellcurrency,
						 user_buycurrency, mouseClick_fn) {

	sellinput = document.getElementById('sellInput');
	sellinput.value = user_sell_amt;

	sellcurrency = document.getElementById('step2_select2');
	sellcurrency.value = 'USD';

	buycurrency = document.getElementById('step2_select3');
	buycurrency.value = 'GBP';

	btn = document.getElementById('getRateBtn');
	mouseClick_fn(btn);
}

var pageload_count = 0
page.onLoadFinished = function (status){
	console.log('Status: ' + status);
	console.log('Page Title: ' + page.title)
	console.log('iterator: ' + pageload_count)

	if(pageload_count==0){
		page.evaluate(fillLoginInfo, fx_password);
		pageload_count++;
	}
	else if (pageload_count==1) {
		// Currency Home
		var sell_amt = 1000;
		var sellcurrency = 'USD';
		var buycurrency = 'GBP';
		page.evaluate(get_rate, sell_amt, sellcurrency,
					  buycurrency, mouseClick);
		page.render('torfx_screenshot.png');
		fs.write('torfx_quote.html', page.content, 'w');
		page.evaluate(logout, mouseClick);
		phantom.exit();
	}
}
page.open('https://online.torfx.com/CustomerPortal/login.htm')