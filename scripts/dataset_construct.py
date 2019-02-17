from urllib import request, parse
from bs4 import BeautifulSoup
import pandas as pd
import wikipedia
import os
import re


class Candidate:
    def __init__(self, name, state, election, year):
        self.name = name
        self.comment = {}
        for topic in topics:
            self.comment[topic] = ""

        self.state = state
        self.election = election
        self.year = year

        try:
            self.bio = wikipedia.summary(self.name.replace('_', ' '), sentences=2)
        except Exception as e:
            print(str(e))
            self.bio = 'nan'

        self.link = 'https://ballotpedia.org/{}'.format(self.name)


def html_wrangle(df, candidate, topic, element):
    if candidate.election == 'presidential':
        filename = '{}_{}'.format(candidate.name, topic)
        raw_html = open('../data/{}/{}/{}.txt'.format(candidate.election, candidate.name, filename)).read()

        html = BeautifulSoup(raw_html, 'html.parser')

        # kill all script and style elements
        for script in html(["script", "style"]):
            script.decompose()  # rip it out

        for p in html.select(element):
            comment = re.sub(r'\\[a-z]', '', p.text)

            # 'name', 'topic', 'comment', 'state', 'election', 'bio', 'link'
            df = df.append(pd.Series(
                [candidate.name, candidate.party, topic, comment, candidate.state, candidate.election, candidate.bio, candidate.link],
                index=df.columns), ignore_index=True)

        return df

    elif candidate.election == 'house':
        raw_html = open('../data/{}/{}.txt'.format(candidate.election, candidate.name)).read()

        html = BeautifulSoup(raw_html, 'html.parser')

        # kill all script and style elements
        for script in html(["script", "style"]):
            script.decompose()  # rip it out

        for p in html.select(element):
            comment = re.sub(r'\\[a-z]', '', p.text)

            topic, comment = comment.replace('On ', '').split(':  ')

            # # 'name', 'topic', 'comment', 'state', 'election', 'bio', 'link'
            df = df.append(pd.Series(
                [candidate.name, candidate.party, topic, comment, candidate.state, candidate.election, candidate.bio, candidate.link],
                index=df.columns), ignore_index=True)

        return df

    elif candidate.election == 'senate':
        raw_html = open('../data/{}/{}.txt'.format(candidate.election, candidate.name)).read()

        html = BeautifulSoup(raw_html, 'html.parser')

        # kill all script and style elements
        for script in html(["script", "style"]):
            script.decompose()  # rip it out

        for p in html.select(element):
            comment = re.sub(r'\\[a-z]', '', p.text)

            topic, comment = comment.replace('On ', '').split(':  ')

            # # 'name', 'topic', 'comment', 'state', 'election', 'bio', 'link'
            df = df.append(pd.Series(
                [candidate.name, candidate.party, topic, comment, candidate.state, candidate.election, candidate.bio, candidate.link],
                index=df.columns), ignore_index=True)

        return df

    elif candidate.election == 'gov':
        raw_html = open('../data/{}/{}.txt'.format(candidate.election, candidate.name)).read()

        html = BeautifulSoup(raw_html, 'html.parser')

        # kill all script and style elements
        for script in html(["script", "style"]):
            script.decompose()  # rip it out

        for p in html.select(element):
            comment = re.sub(r'\\[a-z]', '', p.text)

            topic, comment = comment.replace('On ', '').split(':  ')

            # # 'name', 'topic', 'comment', 'state', 'election', 'bio', 'link'
            df = df.append(pd.Series(
                [candidate.name, candidate.party, topic, comment, candidate.state, candidate.election, candidate.bio, candidate.link],
                index=df.columns), ignore_index=True)

        return df


def scrap_topic(df, candidate, topic):
    if candidate.election == 'presidential':
        url = 'http://www.ontheissues.org/{}/{}_{}.htm'.format(candidate.year, candidate.name, topic)

        try:
            headers = {}
            headers['User-Agent'] = """
            Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
            Chrome/24.0.1312.27 Safari/537.17"""

            req = request.Request(url, headers=headers)
            resp = request.urlopen(req)

            respData = resp.read()
            saveFile = open('../data/{}/{}/{}_{}.txt'.format(candidate.election, candidate.name, candidate.name, topic),
                            'w')
            saveFile.write(str(respData))
            saveFile.close()

            df = html_wrangle(df, candidate, topic, 'h3')
            # print(df.head())

            return df, False

        except Exception as e:
            print(candidate.name + '\t' + str(e))
            return df, True

    elif candidate.election == 'house':
        url = 'http://www.ontheissues.org/Archive/{}_{}_{}.htm'.format('House', candidate.state, candidate.name)

        try:
            headers = {}
            headers['User-Agent'] = """
            Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
            Chrome/24.0.1312.27 Safari/537.17"""

            req = request.Request(url, headers=headers)
            resp = request.urlopen(req)

            respData = resp.read()
            saveFile = open('../data/{}/{}.txt'.format(candidate.election, candidate.name), 'w')
            saveFile.write(str(respData))
            saveFile.close()

            df = html_wrangle(df, candidate, topic, 'h3')
            return df, False

        except Exception as e:
            print(candidate.name + '\t' + str(e))
            return df, True

    elif candidate.election == 'senate':
        # Archive / 2018_CA_Senate_Dianne_Feinstein.htm
        url = 'http://www.ontheissues.org/Archive/{}_{}_Senate_{}.htm'.format(candidate.year, candidate.state, candidate.name)

        try:
            headers = {}
            headers['User-Agent'] = """
            Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
            Chrome/24.0.1312.27 Safari/537.17"""

            req = request.Request(url, headers=headers)
            resp = request.urlopen(req)

            respData = resp.read()
            saveFile = open('../data/{}/{}.txt'.format(candidate.election, candidate.name), 'w')
            saveFile.write(str(respData))
            saveFile.close()

            df = html_wrangle(df, candidate, topic, 'h3')
            return df, False

        except Exception as e:
            print(candidate.name + '\t' + str(e))
            return df, True

    elif candidate.election == 'gov':
        # Archive / 2018_CA_Senate_Dianne_Feinstein.htm
        url = 'http://www.ontheissues.org/Archive/{}_{}_Gov_{}.htm'.format(candidate.year, candidate.state, candidate.name)

        try:
            headers = {}
            headers['User-Agent'] = """
            Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
            Chrome/24.0.1312.27 Safari/537.17"""

            req = request.Request(url, headers=headers)
            resp = request.urlopen(req)

            respData = resp.read()
            saveFile = open('../data/{}/{}.txt'.format(candidate.election, candidate.name), 'w')
            saveFile.write(str(respData))
            saveFile.close()

            df = html_wrangle(df, candidate, topic, 'h3')
            return df, False

        except Exception as e:
            print(candidate.name + '\t' + str(e))
            return df, True


def generate_dataset(election):
    df = pd.DataFrame(columns=['name', 'party', 'topic', 'comment', 'state', 'election', 'bio', 'link'])
    if election == 'presidential':
        candidates = open('../data/{}/url_candidates.txt'.format(election), 'r').read().splitlines()

        for name in candidates:
            year = 2016
            candidate = Candidate(name=name, party='nan', state='nan', election=election, year=year)

            for topic in topics:
                print(name, topic)

                df, error = scrap_topic(df, candidate, topic)

                if error:
                    break

    elif election == 'house':
        load_file = open('../data/{}/ucandidates.txt'.format(election), 'r').read().splitlines()
        year = 2018

        for line in load_file:
            if not line:
                continue

            name, state, party = line.split(',')
            if party not in ['Democrat', 'Republican']:
                party = 'Independent'

            candidate = Candidate(name=name, state=state, election=election, year=year)
            candidate.party = party

            for topic in topics:
                print(name, topic)
                df, error = scrap_topic(df, candidate, topic)

                if error:
                    break

    elif election == 'senate':
        load_file = open('../data/{}/ucandidates.txt'.format(election), 'r').read().splitlines()
        year = 2018

        for line in load_file:
            if not line:
                continue

            name, state, party = line.split(',')
            if party not in ['Democrat', 'Republican']:
                party = 'Independent'

            candidate = Candidate(name=name, state=state, election=election, year=year)
            candidate.party = party

            for topic in topics:
                print(name, topic)
                df, error = scrap_topic(df, candidate, topic)

                if error:
                    break

    elif election == 'gov':
        load_file = open('../data/{}/ucandidates.txt'.format(election), 'r').read().splitlines()
        year = 2018

        for line in load_file:
            if not line:
                continue

            try:
                name, state, party = line.split(',')
            except Exception as e:
                print(str(e))
                continue

            if party not in ['Democrat', 'Republican']:
                party = 'Independent'

            candidate = Candidate(name=name, state=state, election=election, year=year)
            candidate.party = party

            for topic in topics:
                print(name, topic)
                df, error = scrap_topic(df, candidate, topic)

                if error:
                    break

    df.to_csv('../data/{}.csv'.format(election), index=False)
    df.to_json('../data/{}.json'.format(election), orient='records')


if __name__ == '__main__':
    elections = ['presidential', 'house', 'senate', 'gov']
    topics = open('../data/topics.txt', 'r').read().splitlines()

    zipcodes = pd.read_csv('../data/us-zipcode.csv', low_memory=False)
    states = zipcodes.State.unique()

    generate_dataset(elections[3])

    # for election in elections:
    #     generate_dataset(election)



