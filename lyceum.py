import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
from queue import Queue
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://liceum.cv.ua"
search_obj = input('Enter search object: ')
q = Queue()
q.put(url)
used = [url]
count = 0
sum = 0
while not (q.empty()):
    count+=1;
    cur_url = q.get()
    print('Retrieving', cur_url)
    try:
        handle = urllib.request.urlopen(cur_url, context=ctx)
        html = handle.read().decode()
    except:
        print('Wrong page')
        continue
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a'):
        new_url = link.get('href')
        if new_url is None:
            continue
        if new_url.startswith("http://liceum.cv.ua") and not new_url.startswith("http://liceum.cv.ua/wp-content/") and new_url not in used:
            q.put(new_url)
            used.append(new_url)
            used.append(new_url+"#respond")
    text=soup.get_text()
    occur = re.findall(search_obj, text)
    sum+=len(occur)
    print("Have found there", len(occur), "matches,", "so far there is", sum)
print("=======Done! Have visited", count, "pages")
