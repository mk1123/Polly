from bs4 import BeautifulSoup
import os
import re
import sys

sys.stdout = open("../data/ots_wrangled.txt", "w")


raw_html = open('../data/withHeaders.txt').read()
html = BeautifulSoup(raw_html, 'html.parser')
for p in html.select('*'):
    # print(re.findall(r'\\[a-z]', p.text))
    print(re.sub(r'\\[a-z]', '', p.text))

