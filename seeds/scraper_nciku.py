from bs4 import BeautifulSoup
import requests
import codecs

url = "http://www.nciku.com/theme/detail?catg2ID=14&initial=&page=5"

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data)

entries = soup.select('li.theme_list_box')

f = codecs.open('food_words.txt', mode='a', encoding='utf-8')
tok = u'|||'

for entry in entries:
    chin = entry.select("li.theme_txt_cn_l")[0]
    eng = entry.select("li.theme_txt_en_l")[0]

    links = chin.find_all('a')
    span = links[0].find_all('span')
    chin_chars = span[0].string.strip()

    links = eng.find_all('a')
    if links != []:
        eng_text = links[0].string.strip()
    else: 
        eng_text = eng.string.strip()

    print chin_chars, eng_text
    entry_string = "%s %s %s \n" % (chin_chars, tok, eng_text)
    entry_string.encode('utf-8')
    f.write(entry_string)


f.close()