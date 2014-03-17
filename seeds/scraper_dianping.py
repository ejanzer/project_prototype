from bs4 import BeautifulSoup
import requests
import codecs

for i in range(1, 15):

    url = "http://www.dianping.com/search/category/2/10/g246p%d" % i

    r = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data)

    features = soup.select('li.features')

    f = codecs.open('dianping_tags.txt', mode='a', encoding='utf-8')
    tok = u'|||'

    for feature in features:
        links = feature.find_all('a')
        link = links[0]
        chars = link.find_all(text=True)
        chars.append('\n')
        chars = ''.join(chars)
        print chars
        chars.encode('utf-8')
        f.write(chars)


    f.close()