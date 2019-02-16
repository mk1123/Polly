from urllib import request, parse
from bs4 import BeautifulSoup
import os
import re

candidates = open('../data/url_candidates.txt', 'r')


def html_wrangle(candidate):
    raw_html = open('../data/{}.txt'.format(candidate)).read()
    html = BeautifulSoup(raw_html, 'html.parser')

    with open('../data/{}.txt'.format(candidate), 'w') as file:
        # kill all script and style elements
        for script in html(["script", "style"]):
            script.decompose()  # rip it out

        '''
        # get text
        text = html.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        '''

        for p in html.select('*'):
            file.write(re.sub(r'\\[a-z]', '', p.text))


def scrap_page(candidate):
    # print('http://www.ontheissues.org/{}.htm'.format(candidate))

    # Avoid web scraper bot detections
    try:
        x = request.urlopen('http://www.ontheissues.org/{}.htm'.format(candidate))
        print(x.read())

    except Exception as e:
        print(str(e))

    try:
        url = 'http://www.ontheissues.org/{}.htm'.format(candidate)
        headers = {}
        headers['User-Agent'] = """
        Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
        Chrome/24.0.1312.27 Safari/537.17"""

        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)

        respData = resp.read()
        saveFile = open('../data/{}.txt'.format(candidate), 'w')
        saveFile.write(str(respData))
        saveFile.close()

        html_wrangle(candidate)

    except Exception as e:
        print(str(e))
        print(candidate)


if __name__ == '__main__':
    for candidate in candidates:
        scrap_page(candidate[:-1])





