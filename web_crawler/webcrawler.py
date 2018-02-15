from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

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

'''Extract the title of a Page and Clean It'''
def clean_title(title):
    invalid_characters = ['<','>',':','"','/','\\','|','?','*']
    for c in invalid_characters:
        title = title.replace(c, '')
    return title


'''Extract Outgoing(inner) URLS from Page Content'''
def get_urls(soup):
    links = soup.find_all('a')
    urls = []
    for link in links:
        urls.append(link.get('href'))
    return urls


'''Check if a URL is Valid'''
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


seedOne = "/wiki/Information_retrieval"
seedTwo = "/wiki/Information"
relatedTerms = "information search retrieve cognitive memory science method research history review process fact model mapping world content"
seedList = [seedOne, seedTwo]

queue = []
visitedUrls = [];
pageCounter = 0
savedUrlList = []

for url in seedList:
    queue.append(url)
    visitedUrls.append(url)

i = 1
while queue:
    url = queue.pop()
    url = "https://en.wikipedia.org" + url
    pageContent = get_page_content(url)
    if pageContent is None:
        continue
    termCounter = 0
    soup = BeautifulSoup(pageContent, 'html.parser')
    page_text = soup.get_text()
    
    for term in relatedTerms.split():
        '''Check whether a term is included in the page text'''
        if re.search(term, page_text, re.I):
            termCounter = termCounter + 1
            if termCounter >= 2:
                   title = soup.title.string
                   pageTitle = clean_title(title)
                   #In case, place save function here!
                   savedUrlList.append(url)
                   pageCounter = pageCounter + 1
                   print("page " + str(pageCounter) + ": " + url)
                   break
    if pageCounter >= 500:
        break
    
    outGoingUrls = get_urls(soup)
    for outGoingUrl in outGoingUrls:
        if is_url_valid(outGoingUrl) and outGoingUrl not in visitedUrls:
            queue.append(outGoingUrl)
            visitedUrls.append(outGoingUrl)
    
f = open("crawled_urls.txt","w")
i = 1
for url in savedUrlList:
    f.write(str(i) + ': ' + url + '\n')
    i += 1
f.close()       
