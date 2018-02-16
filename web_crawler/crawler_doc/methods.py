
'''

'''Parse Page Content Using Beautiful Soup'''
soup = BeautifulSoup(page_content, 'html.parser')

'''Extract Main Text of a Page'''
page_text = soup.get_text()

'''Extract the title of a Page and Clean It'''
title = soup.title.string
title = clean_title(title)

def clean_title(title):
    invalid_characters = ['<','>',':','"','/','\\','|','?','*']
    for c in invalid_characters:
        title = title.replace(c, '')
    return title

'''Check whether a term is included in the page text'''
if re.search(term, page_text, re.I):
    print("hello world")

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
    match = re.search('^/wiki/',url)
    if match:
        return True
    else:
        return False

'''Reformat URL, Change a relative URL into a full URL'''
def reformat_url(url):
    match = re.search('^/wiki/',url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url

'''Save a page'''
def save(text, path):
    f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
    f.write(text)
    f.close()

'''Save Crawled URLS'''
f = open("crawled_urls.txt","w")
i = 1
for url in crawled_urls:
    f.write(str(i) + ': ' + url + '\n')
    i += 1
f.close()

'''
