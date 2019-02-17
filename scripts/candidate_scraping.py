from urllib import request, parse
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def html_wrangle(df, election, name, topic, element='*'):
    print(len(df.index))
    filename = '{}_{}'.format(name, topic)
    raw_html = open('../data/{}/{}/{}.txt'.format(election, name, filename)).read()
    html = BeautifulSoup(raw_html, 'html.parser')

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

    for p in html.select(element):
        comment = re.sub(r'\\[a-z]', '', p.text)
        df = df.append(pd.Series([name, comment, topic], index=df.columns), ignore_index=True)

    return df


def scrap_page(election, candidate):
    # print('http://www.ontheissues.org/{}.htm'.format(candidate))

    # Avoid web scraper bot detections
    try:
        x = request.urlopen('http://www.ontheissues.org/{}.htm'.format(candidate))
        # print(x.read())

    except Exception as e:
        print(candidate + '\t' + str(e))
        return False

    try:
        url = 'http://www.ontheissues.org/{}.htm'.format(candidate)
        headers = {}
        headers['User-Agent'] = """
        Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
        Chrome/24.0.1312.27 Safari/537.17"""

        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)

        respData = resp.read()
        saveFile = open('../data/{}/{}/{}.txt'.format(election, candidate, candidate), 'w')
        saveFile.write(str(respData))
        saveFile.close()

        # html_wrangle(candidate)

        return True

    except Exception as e:
        print(candidate + '\t' + str(e))
        return False


def scrap_topic(df, election, candidate, year, topic):
    print('http://www.ontheissues.org/{}/{}_{}.htm'.format(year, candidate, topic))

    # Avoid web scraper bot detections
    try:
        x = request.urlopen('http://www.ontheissues.org/{}/{}_{}.htm'.format(year, candidate, topic))
        # print(x.read())

    except Exception as e:
        print(candidate + '\t' + str(e))
        return False

    try:
        url = 'http://www.ontheissues.org/{}/{}_{}.htm'.format(year, candidate, topic)
        headers = {}
        headers['User-Agent'] = """
        Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
        Chrome/24.0.1312.27 Safari/537.17"""

        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)

        respData = resp.read()
        saveFile = open('../data/{}/{}/{}_{}.txt'.format(election, candidate, candidate, topic), 'w')
        saveFile.write(str(respData))
        saveFile.close()

        df = html_wrangle(df, election, candidate, topic, 'h3')
        print(df.head())
        return df

    except Exception as e:
        print(candidate + '\t' + str(e))
        return False


if __name__ == '__main__':

    election = 'presidential'
    candidates = open('../data/{}/url_candidates.txt'.format(election), 'r').read().splitlines()
    topics = open('../data/topics.txt', 'r').read().splitlines()

    for candidate in candidates:
        if scrap_page(election, candidate):
            error = False
            df = pd.DataFrame(columns=['Name', 'Comment', 'Topic'])

            for topic in topics:
                print(candidate, topic)
                df = scrap_topic(df, election, candidate, '2016', topic)

                if isinstance(df, bool):
                    error = True
                    break

            if not error:
                print(df.head())
                df.to_csv('../data/{}/{}.csv'.format(election, candidate), index=False)
                df.to_json('../data/{}/{}.json'.format(election, candidate), orient='records')






