from bs4 import BeautifulSoup
import requests
import codecs
import re

def contains_alpha(string):
    not_whitespace = re.compile('\S+')
    if re.search(not_whitespace, string):
        return True
    else:
        return False

url = "http://mandarin.about.com/od/vocabulary/a/voc_dishes.htm"

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

entries = soup.find_all('tr')


f = codecs.open('dishes.txt', mode='a', encoding='utf-8')
tok = u'|||'

# skip the table header by starting at 1.
for i in range(1, len(entries)):
    tds = entries[i].find_all('td')
    chin = tds[2].string
    eng = tds[0].string

    if contains_alpha(eng) and contains_alpha(chin):
        chin = chin.strip()
        eng = eng.strip()
        print chin, eng
        entry_string = "%s %s %s \n" % (chin, tok, eng)
        entry_string.encode('utf-8')
        f.write(entry_string)


f.close()