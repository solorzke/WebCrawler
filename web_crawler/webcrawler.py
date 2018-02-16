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
    if re.search('/wiki/User_talk:', url):
        return False
    if re.search('/wiki/Main_Page', url):
        return False
    match = re.search('^/wiki/',url)
    if match:
        return True
    else:
        return False

'''Save a page'''
def save(text, path):
    f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
    f.write(text)
    f.close()


seedOne = "/wiki/Video_game"
seedTwo = "/wiki/Virtual_reality"
relatedTerms = " gaming , xbox , playstation , console , jrpg , rpg , sega , nintendo , gpu , video-game , cartridge , controller , oculus , vive , halo , bungie , usb , disk , valve , pc , dualshock , gameboy , arcade , graphics , atari "
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
    url = queue.pop(0)
    url = "https://en.wikipedia.org" + url
    pageContent = get_page_content(url)
    if pageContent is None:
        continue
    termCounter = 0
    soup = BeautifulSoup(pageContent, 'html.parser')
    page_text = soup.get_text()
    
    for term in relatedTerms.split(','):
        '''Check whether a term is included in the page text'''
        if term in page_text.lower():
            #print("Current term: " + term + " url: " + url)
            termCounter = termCounter + 1
            if termCounter >= 2:
                   title = soup.title.string
                   pageTitle = clean_title(title)
                   #In case, place save function here!
                   save(str(soup), 'crawled_html_pages/' + pageTitle + '.html') 
                   savedUrlList.append(pageTitle + "\n" + url)
                   pageCounter = pageCounter + 1
                   print("page " + str(pageCounter) + ": " + pageTitle +"\n" + url)
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
tof = False
for url in savedUrlList:
    strcleaned = ''.join([x for x in url if ord(x) < 128])
    f.write(str(i) + ": " + strcleaned + "\n\n")
    i = i + 1
    '''
    if i % 2 == 0:
        f.write(strcleaned)
        f.write("\n\n")
        continue
    
    else:
        f.write(str(i) + ': ' + strcleaned)
        f.write("\n")
        i = i + 1
        continue
    '''    
f.close()       
