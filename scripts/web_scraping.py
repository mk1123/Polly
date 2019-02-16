from urllib import request, parse

# Avoid web scraper bot detections
try:
    x = request.urlopen('http://www.ontheissues.org/default.htm')
    print(x.read())

except Exception as e:
    print(str(e))

try:
    url = 'http://www.ontheissues.org/default.htm'
    headers = {}
    headers['User-Agent'] = """
    Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)
    Chrome/24.0.1312.27 Safari/537.17"""

    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)

    respData = resp.read()
    saveFile = open('../data/withHeaders.txt', 'w')
    saveFile.write(str(respData))
    saveFile.close()

except Exception as e:
    print(str(e))
