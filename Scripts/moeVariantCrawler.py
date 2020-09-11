import aiohttp
import asyncio
import requests
import json
import os
import re
from bs4 import BeautifulSoup

"""
- 有些字是用圖片表示的，如 C00003
- 有些編號不存在，如 C00381, C02837

本典正字主要依據教育部常用字、次常用字、罕用字三個標準字體表；遇有具有獨立音義而三字表未收之文獻字形，
則補收為新正字。各字級字數為：常用字4,808字、次常用字6,329字、罕用字18,319字、新正字465字。

三、	本字典所收正字，皆列有字號，以表其來源。字號中之英文字母，
「A」表常用字，「B」表次常用字，「C」表罕用字，「N」則為新增正字。
ABC三英文字母后之數字，為原字表之字號。N字母后之數字，則為編輯小組依收錄時間先後所排流水序號。
"""

wordDataList = []
characterData = []
enableDownload = False

normalList_continuous_re = re.compile(r'\(\S\)(\S+)')
normalList_re = re.compile(r'\(\S\)([^\(\)]+)')

# e.g., (1), (2), (3)
numberList_re = re.compile(r'\(\d\)')


def Clean(string):
    # https://blog.csdn.net/IAlexanderI/article/details/79455027
    # \xa0 是不間斷空白符 &nbsp; # \u3000 是全角的空白符 # 通常所用的空格是 \x20
    return string.replace(" ", "").replace(
        "\u3000", "").replace("\xa0", "")


def ParseByTableName(soup, tableName):
    valueElement = soup.findAll('span', text=re.compile(tableName))[
        0].parent.find_next_sibling("td")
    return valueElement.text


def ParseListByTableName(soup, tableName, seperator):
    value = ParseByTableName(soup, tableName)
    valueList = seperator.findall(
        value) if seperator.findall(value) else [value]
    return valueList


def ParsePinyin(soup):
    return ParseListByTableName(soup, "漢語拼音", normalList_continuous_re)


def ParseExplain(soup):
    return ParseByTableName(soup, "說文釋形")


def ParseWord(soup, serial):
    rawWord = ParseByTableName(soup, "正字")
    word = re.match(r"【(\S+)】", rawWord)
    if not word:
        #print(f"parse word {serial} failed")
        if serial in characterData:
            word = characterData[serial]
            #print(f"use word {word}")
    else:
        word = word.group(1)
    for img in soup.find_all("img"):
        img.replaceWith(word)
    return word


def ParseBopomofo(soup):
    rawBopomofo = ParseByTableName(soup, "注音")

    rawBopomofoList = re.findall(r"(\(\S+\)\s*\S+)", rawBopomofo) if re.findall(
        r"(\(\S+\)\s*\S+)", rawBopomofo) else [rawBopomofo]
    rawBopomofoList = [Clean(b) for b in rawBopomofoList]
    rawBopomofoList = [b.replace("（又音）", "")
                       for b in rawBopomofoList]  # 避免替換括號時出錯

    bopomofoList = normalList_re.findall(
        rawBopomofo) if normalList_re.findall(rawBopomofo) else [rawBopomofo]
    bopomofoList = [Clean(b) for b in bopomofoList]

    return rawBopomofoList, bopomofoList


def bopomofoToRE(bopomofo):
    bopomofo = bopomofo.replace(" ", "")
    if ")" in bopomofo:
        bopomofo = bopomofo.replace(")", "[）)]")
    elif "）" in bopomofo:
        bopomofo = bopomofo.replace("）", "[）)]")
    else:
        return bopomofo

    if "（" in bopomofo:
        bopomofo = bopomofo.replace("（", "[(（]")
    elif "(" in bopomofo:
        bopomofo = bopomofo.replace("(", "[(（]")
    else:
        return bopomofo

    index = bopomofo.find(")")
    bopomofo = bopomofo[:index+2] + \
        "\\s*" + bopomofo[index+2:]
    return bopomofo


def jprint(jsondata):
    print(json.dumps(jsondata, indent=4, ensure_ascii=False))


def ParseMeaning(soup, rawBopomofoList, bopomofoList, serial):
    # 用注音分段
    meaning = ParseByTableName(soup, "釋義")
    meaning = numberList_re.sub("", meaning)
    meaning = Clean(meaning)
    rawBopomofoList_escape = [bopomofoToRE(b) for b in rawBopomofoList]

    bopomofo_re = re.compile("|".join(rawBopomofoList_escape))

    meaningList = bopomofo_re.split(meaning)
    if len(meaningList) == 1:
        meaningList = [meaning]
    else:
        meaningList = list(
            filter(lambda x: Clean(x), meaningList))
    for i in range(len(meaningList)):
        meaningList[i] = Clean(bopomofo_re.sub(
            "", meaningList[i]))
    if len(meaningList) != len(rawBopomofoList):
        print(f"-----------{serial}------------")
        print(rawBopomofoList_escape)
        print(bopomofo_re)
        print(meaning)
        jprint(bopomofo_re.split(meaning))
        jprint(meaningList)
        print("--------------------------------")
    return meaningList


def ParseContent(content, serial):
    soup = BeautifulSoup(content, features="html.parser")
    try:
        meaning = []

        word = ParseWord(soup, serial)
        raw_bopomofo, bopomofo = ParseBopomofo(soup)
        pinyin = ParsePinyin(soup)
        meaning = ParseMeaning(soup, raw_bopomofo, bopomofo, serial)
        # useless
        wordElement = soup.findAll('span', text=re.compile('正字'))[
            0].parent.find_next_sibling("td")
        radical = wordElement.find_next_sibling("td").select_one(".radical")
        radical = radical.text
        stroke1 = wordElement.find_next_sibling("td").select_one(
            ".radical").find_next_sibling("span")
        stroke1 = int(stroke1.text)
        stroke2 = wordElement.find_next_sibling("td").select_one(
            ".radical").find_next_sibling("span").find_next_sibling("span")
        stroke2 = int(stroke2.text)
        explain = ParseExplain(soup)

        meanings = [{"bopomofo": b, "pinyin": p,
                     "meaning": m} for (b, m, p) in zip(bopomofo, meaning, pinyin)]

        wordData = {
            "serial": serial,
            "word": word,
            "radical": radical,
            "meanings": meanings,
            "explain": explain,
            "stroke1": stroke1,
            "stroke2": stroke2
        }

        wordDataList.append(wordData)
    except Exception as e:
        print(e)
        print(f"Parse Error: serial {serial}")
        if bopomofo:
            print(bopomofo)
        if raw_bopomofo:
            print(raw_bopomofo)
        if meaning:
            print("\n".join(meaning))


async def CrawlContent(url, fileName):
    print(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.text()
            if resp.status != 200:
                print(f"Error: Response get {resp.status}")
                content = ""

    if not content:
        return
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(content)
    return content


def GetRunningTasksCount():
    return len([task for task in asyncio.all_tasks() if not task.done()])


codes = ["A", "B", "C", "N"]
wordCount = {"A": 5000, "B": 6500, "C": 20000,
             "N": 600}
loop = asyncio.get_event_loop()
concurrentCount = 10
tasks = []
platform = "windows"
# platform = "linux"
folderName = "異體字" if platform == "windows" else "variants"


def GetMaxWordCount(code):
    return 50 if platform == "windows" else wordCount[code]


async def main():
    global characterData
    with open("variant-wordCharacter.json", encoding="utf-8") as f:
        characterData = json.loads(f.read())
    for code in codes:
        serial = 1
        for serial in range(1, GetMaxWordCount(code)):
            fileName = f"{folderName}/{code}{serial:05}.txt"
            if os.path.exists(fileName):
                with open(fileName, encoding="utf-8") as f:
                    content = f.read()
                ParseContent(content, f"{code}{serial:05}")
            else:
                if not enableDownload:
                    continue
                url = f"http://dict.variants.moe.edu.tw/variants/rbt/word_attribute.rbt?educode={code}{serial:05}"
                while GetRunningTasksCount() >= concurrentCount:
                    # Wait for some download to finish before adding a new one
                    print(
                        f"{GetRunningTasksCount()} running tasks, waiting...")
                    await asyncio.wait(
                        tasks, return_when=asyncio.ALL_COMPLETED)
                task = loop.create_task(CrawlContent(url, fileName))
                tasks.append(task)

    if len(tasks) > 0:
        await asyncio.wait(tasks)

loop.run_until_complete(main())
open("variant-WordData.json", "w",
     encoding="utf-8").write(json.dumps(wordDataList, indent=4, ensure_ascii=False))
