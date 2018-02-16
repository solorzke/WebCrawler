from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os


seedOne = "https://en.wikipedia.org/wiki/3D_bioprinting"
seedTwo = "https://en.wikipedia.org/wiki/Organ_transplantation"
keywords = "organ print 3-d biology bioprinting transplant doctor research experiment"

seedList = [seedOne, seedTwo]

queue = []
visitedUrls = [];
pagecounter = 0
savedUrlList = []

for url in seedList:
    queue.append(url)
    visitedUrls.append(url)


'''Setting up SSL environment'''
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

'''Getting page content'''
def get_page_content(url):
    try:
        html_response_text = urlopen(url).read()
        page_content = html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None


'''Save a page'''
def save(text, path):
    f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
    f.write(text)
    f.close()


url = "https://en.wikipedia.org/wiki/Video_game"
pageContent = get_page_content(url)

soup = BeautifulSoup(pageContent, 'html.parser')

'''Extract Main Text of a Page'''
page_text = soup.get_text()

print(soup)

'''Extract the title of a Page and Clean It'''
def clean_title(title):
    invalid_characters = ['<','>',':','"','/','\\','|','?','*']
    for c in invalid_characters:
        title = title.replace(c, '')
    return title

title = soup.title.string
title = clean_title(title)
#save(str(soup), '/Users/Kevin/Desktop/web_crawler/crawled_html_pages/' + title + '.html')
strd = "she \n sdfd"
#print(strd.splitlines())
#print(title)


term = " syntax "
term = term.lower()
'''
if term in page_text.lower():
    print("ywe")
else:
    print("ffd")

if re.search(term, page_text, re.I):
    print("eh")
else:
    print("dfd")
'''
'''
ter = 0
keywords = "information search retrieve cognitive memory science method research history review process fact model mapping world content"
for term in keywords.split():
    if re.search(term, page_text, re.I):
        ter += 1
        if ter <= 2:
            print(term)
    else:
        continue
        '''
'''
relatedTerms = "organ print 3-d biology bioprinting transplant doctor research experiment"
for term in relatedTerms.split():
    if re.search(term, page_text, re.I):
        print(term)
'''

'''Extract Outgoing(inner) URLS from Page Content'''
def get_urls(soup):
    links = soup.find_all('a')
    urls = []
    for link in links:
        urls.append(link.get('href'))
    return urls

'''Check if a URL is Valid'''
def is_url_valid(url):
    if url is None:
        return False
    if re.search('#', url):
        return False
    if re.search('/wiki/Wikipedia:', url):
        return False
    if re.search('/wiki/Special:', url):
        return False
    if re.search('/wiki/Talk:', url):
        return False
    if re.search('/wiki/Help:', url):
        return False
    if re.search('/wiki/File:', url):
        return False
    if re.search('/wiki/Category:', url):
        return False
    if re.search('/wiki/Template', url):
        return False
    if re.search('/wiki/Portal:', url):
        return False
    match = re.search('^/wiki/',url)
    if match:
        return True
    else:
        return False



'''
outGoingUrls = get_urls(soup)
for url in outGoingUrls:
    if is_url_valid(url):
        print(url)
'''
