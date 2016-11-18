For the first time in **many** years I've joined a [Fantasy Football league](http://www.espn.com) with some of my family. One of the reasons I have not engaged in the Fantasy football is that, frankly, I'm not very good. In fact, I'm pretty bad. I have a passing interest in Football, but my interests lie more with Baseball than football (especially in light of the NFLs policy on punishing players for some infractions of league rules, but not punishing them for infractions of societal norms (see Tom Brady and Ray Lewis respectively). 

That being said, I am in a Fantasy Football league this year, and as of this writing am a respectable 5-5 and only 2 games back from making the playoffs with 3 games left. 

This means that what I started on yesterday I really should have started on much sooner, but I didn't.

I had been counting on ESPN's 'projected points' to help guide me to victory ... it's working about as well as flipping a coin (see my record above).

I had a couple of days off from work this week and some time to tinker with Python, so I thought, what the hell, let's see what I can do.

Just to see what other people had done I did a quick [Google Search](http://www.google.com) and found [someone that had done what I was trying to do with data from the NBA in 2013](http://danielfrg.com/blog/2013/04/01/nba-scraping-data/).

Using their post as a model I set to work. 

The basic strategy I am mimicking is to:

* Get the Teams and put them into a dictionary
* Get the 'matches' and put them into a dictionary
* Get the player stats and put them into a dictionary for later analysis

I start of importing some standard libraries `pandas`, `requests`, and `BeautifulSoup` (the other libraries are for later).

```
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
from datetime import datetime, date
```

Next, I need to set up some variables. [`BeautifulSoup` is a Python library for pulling data out of HTML and XML files.](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). It's pretty sweet. The code below is declaring a URL to scrape and then users the `requests` library to get the actual `HTML` of the page and put it into a variable called `r`. 

```
url = 'http://espn.go.com/nfl/teams'
r = requests.get(url)
```

`r` has a method called `text` which I'll use with `BeautifulSoup` to create the `soup`. The `'lxml'` declares the parser type to be used. The default is `lxml` and when I left it off I was presented with a warning, so I decided to explicitly state which parser I was going to be using to avoid the warning.  

```
soup = BeautifulSoup(r.text, 'lxml')
```

Next I use the `find_all` function from `BeautifulSoup`. The cool thing about `find_all` is that you can either pass just a tag element, i.e. `li` or `p`, but you can add an additional `class_` argument (notice the underscore at the end ... I  missed it more than once and got an error because `class` is a keyword used by `Python`). Below I'm getting all of the `ul' elements of the class type 'medium-logos'.

```
tables = soup.find_all('ul', class_='medium-logos')
```

Now I set up some `list` variables to hold the items I'll need for later use to create my `dictionary`

```
teams = []
prefix_1 = []
prefix_2 = []
teams_urls = []
```

Now, we do some *actual* programming:

Using a nested `for` loop to find all of the `li` elements in the variable called `lis` which is based on the variable `tables` (recall this is all of the `HTML` from the page I scrapped that has *only* the tags that match `<ul class='medium-logos></ul>` and all of the content between them).

The nested `for` loop creates 2 new variables which are used to populate the 4 lists from above. The creating of the `info` variable gets the a tag from the li tags. The `url` variable takes the `href` tag from the `info` variable. In order to add an item to a list (remember, all of the lists above are empty at this point) we have to invoke the method `append` on each of the lists with the data that we care about (as we look through). 

The function `split` can be used on a string (which `url` is). It allows you to take a string apart based on a passed through value and convert the output into a list. This is super useful with URLs since there are many cases where we're trying to get to the path. Using `split('/')` allows the URL to be broken into it's constituent parts. The negative indexes used allows you to go from right to left instead of left to right. 

To really break this down a bit, if we looked at just one of the URLs we'd get this:

`http://www.espn.com/nfl/team/_/name/ten/tennessee-titans`

The `split('/')` command will turn the URL into this:

`['http:', '', 'www.espn.com', 'nfl', 'team', '_', 'name', 'ten', 'tennessee-titans']`

Using the negative index allows us to get the right most 2 values that we need. 

```
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        teams_urls.append(url)
        prefix_1.append(url.split('/')[-2])
        prefix_2.append(url.split('/')[-1])
```

Now we put it all together into a dictionary

```
dic = {'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1, 'team': teams}
teams = pd.DataFrame(dic)
```

This is the end of part 1. Parts 2 and 3 will be coming later this week.