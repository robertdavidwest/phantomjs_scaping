import bs4
import ast
'''
Extract friend names from friends.html
'''
soup = bs4.BeautifulSoup(open('friends.html', 'r'))
hyperlinks = soup.findAll('a')
friends = []
for h in hyperlinks:
	try:
		# if data-gt contains 'engagement' then href text is friends name
		data_gt = ast.literal_eval(h.attrs['data-gt'])
		data_gt['engagement']
		print h.text
		friends.append(h.text)
	except KeyError:
		continue

print 'There were {} friends in the html file'.format(len(friends))
