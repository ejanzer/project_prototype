from bs4 import BeautifulSoup
import requests
import codecs

url = "http://www.chinese-tools.com/chinese/vocabulary/list/133/face.html"

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

entries = soup.select('div.ctdico_entry')
entries.extend(soup.select('div.ctdico_entryAlt'))

f = codecs.open('food_words.txt', mode='a', encoding='utf-8')
tok = u'|||'

for entry in entries:
    div = entry.select('.ctdico_char')[0]
    links = div.find_all('a')
    link_strs = []
    for link in links:
        link_strs.append(link.string)
    chin = ''.join(link_strs)
    eng = entry.select('.ctdico_def')[0].string
    print chin, eng
    entry_string = "%s %s %s \n" % (chin, tok, eng)
    entry_string.encode('utf-8')
    f.write(entry_string)


f.close()