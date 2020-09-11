import aiohttp
import asyncio
import requests
import json
import os
import re
from bs4 import BeautifulSoup


codes = ["A", "B", "C", "N"]
wordCount = {"A": 5000, "B": 6500, "C": 20000,
             "N": 600}  # 有些編號真的不存在，如 C00381, C02837

loop = asyncio.get_event_loop()
concurrentCount = 10
tasks = []

enableDownload = True
platform = "windows"
# platform = "linux"
folderName = "異體字字" if platform == "windows" else "variants"
data = {}


def GetMaxWordCount(code):
    # return 50 if platform == "windows" else wordCount[code]
    return wordCount[code]


def GetRunningTasksCount():
    return len([task for task in asyncio.all_tasks() if not task.done()])


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


def Parse(content, codeSerial):
    soup = BeautifulSoup(content, features="html.parser")
    generalSerial = codeSerial[0:4]
    for i in range(0, 100):
        try:
            standard_serial = f"{generalSerial.upper()}{str(i).zfill(2)}"
            serial = f"twedu-{generalSerial}{str(i).zfill(2)}"
            character = soup.findAll('a', title=serial)[0].parent.text[-1]
            data[standard_serial] = character
        except:
            pass


async def main():
    for code in codes:
        for serial in range(1, GetMaxWordCount(code), 100):
            codeSerial = f"{code}{serial:05}"
            fileName = f"{folderName}/{codeSerial}.txt"

            if os.path.exists(fileName):
                with open(fileName, encoding="utf-8") as f:
                    content = f.read()
                Parse(content, codeSerial.lower())
            else:
                if not enableDownload:
                    continue
                    response = requests.get(url)
                url = f"http://zht.glyphwiki.org/wiki/Group:教育部異體字字典-文字一覧{codeSerial.lower()[0:4]}xx"
                print(url)
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
open("variant-wordCharacter.json", "w",
     encoding="utf-8").write(json.dumps(data, indent=4, ensure_ascii=False))
