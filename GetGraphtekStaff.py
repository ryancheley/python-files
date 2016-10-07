import bs4, requests, re

myurl = 'http://www.graphtek.com/Our-Team'

def get_beautiful_soup(url):
	return bs4.BeautifulSoup(requests.get(url).text, "html5lib")
		
soup = get_beautiful_soup(myurl)
tablemgmt = soup.findAll('div', attrs={'id':re.compile('our-team')})

list_of_names = []
for i in tablemgmt:
	for row in i.findAll('span', attrs={'class':'team-name'}):
		text = row.text.replace('<span class="team-name"', '')
		if len(text)>0:
			list_of_names.append(text)
list_of_titles = []
for i in tablemgmt:
	for row in i.findAll('span', attrs={'class':'team-title'}):
		text = row.text.replace('<span class="team-title"', '')
		if len(text)>0:
			list_of_titles.append(text)

print('| Name | Title |')
print('| --- | --- |')
for j, k in zip(list_of_names, list_of_titles):
	print('|'+ j + '|' + k + '|')