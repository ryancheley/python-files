import bs4, requests, re

myurl = 'http://www.graphtek.com/Our-Team'

def get_beautiful_soup(url):
	return bs4.BeautifulSoup(requests.get(url).text, "html5lib")
		
soup = get_beautiful_soup(myurl)
tablemgmt = soup.findAll('div', attrs={'id':re.compile('our-team')})
tableimage = soup.findAll('img', attrs={'class':re.compile('team-pic')})

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

list_of_images = []
for i in range(len(tableimage)):
	text = '![alt text](http://www.graphtek.com/'+tableimage[i]['src']+' "'+tableimage[i]['alt']+'")'
	list_of_images.append(text)

print('| Name | Title | Image |')
print('| --- | --- | --- |')
for j, k, l in zip(list_of_names, list_of_titles, list_of_images):
	print('|'+ j + '|' + k + '|' + l + '|' )

#This is me adding a comment