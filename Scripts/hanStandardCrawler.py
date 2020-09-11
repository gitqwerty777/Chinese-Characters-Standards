import os
import json
import requests
from bs4 import BeautifulSoup

if not os.path.exists("han.html"):
    url = "https://zh.wiktionary.org/zh-hant/Appendix:%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8"
    resp = requests.get(url)
    if resp.status_code != 200:
        print('invalid url:', resp.url)
    with open("han.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    content = resp.text
else:
    with open("han.html", encoding="utf-8") as f:
        content = f.read()

soup = BeautifulSoup(content, 'html.parser')
tables = soup.select(".wikitable")
tableDatas = []
for table in tables:
    tableData = []
    for wordEntry in table.select("tr"):
        data = wordEntry.select("td")
        data = [d.text.strip("\n") for d in data]
        try:
            tableData.append({
                "serial": data[0],
                "word": data[1],
                "bopomofo": data[2]
            })
        except:
            print(wordEntry.select("td"))
            print(data)
    print(f"len to tabledata {len(tableData)}")
    tableDatas.append(tableData)

with open("han-Character.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(tableDatas, ensure_ascii=False))
