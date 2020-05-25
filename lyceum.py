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
while not (q.empty() or count > 75):
    count+=1;
    cur_url = q.get()
    print('Retrieving', cur_url)
    handle = urllib.request.urlopen(cur_url, context=ctx)
    html = handle.read().decode()
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('a'):
        new_url = link.get('href')
        if new_url.startswith("http://liceum.cv.ua") and new_url not in used:
            q.put(new_url)
            used.append(new_url)
    text=soup.get_text()
    occur = re.findall(search_obj, text)
    sum+=len(occur)
    print("Have found", len(occur), "matches,", "sum is", sum)
