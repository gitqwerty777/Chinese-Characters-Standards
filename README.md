# 漢字標準資料

提供中華民國教育部《國字標準字體表》及中華人民共和國教育部《通用規範漢字表》的資料

## 國字標準字體表

臺灣沿用傳統漢字，同時稱之為正體字，其起始標準為中華民國教育部頒布的《常用國字標準字體表》（俗稱「甲表」）所收錄之4808個常用字、《次常用國字標準字體表》（俗稱「乙表」）所錄之6334個常用字（外加9個單位詞，合計6343字）、《罕用字體表》（俗稱「丙表」）所錄之18388個罕用字、以及《原異體字表》（俗稱「丁表」）所收錄之18588個異體字（補遺22字）

### 資料架構

[variant-WordData.json](Data/variant-WordData.json)

``` json
{
    "serial": "A00002",
    "word": "丁",
    "radical": "一",
    "meanings": [
        {
            "bopomofo": "ㄉㄧㄥ",
            "pinyin": "dīng",
            "meaning": "(一)ㄉ一ㄥ1.天干第四位。..."
        },
        {
            "bopomofo": "ㄓㄥ",
            "pinyin": "zhēng",
            "meaning": "「丁丁」，擬聲詞：形容伐木聲。..."
        }
    ],
    "explain": "大徐本：丁，夏時萬物皆丁實。象形。...",
    "stroke1": 1,
    "stroke2": 2
}
```

- `serial`: 異體字字號，注意編號並非完全連續，見[說明](https://dict.variants.moe.edu.tw/variants/rbt/page_content.rbt?pageId=2982208)
- `word`: 單字
- `radical`: 部首
- `meanings`: 陣列，包含 `bopomofo`注音、`pinyin`拼音及`meaning`解釋
- `explain`: 說文釋形
- `stroke1`: 除去部首的筆劃
- `stroke2`: 總筆劃

[variant-WordCharacter.json](Data/variant-WordCharacter.json)

``` json
{
    "A00001": "一"
}
```

- 字號對應文字

### 資料來源

- [異體字字典](https://dict.variants.moe.edu.tw/variants/rbt/page_content.rbt?pageId=2982208)
- [字形維基(GlyphWiki)](http://zht.glyphwiki.org/wiki/)

## 通用規範漢字表

《通用規範漢字表》是由中華人民共和國教育部、國家語言文字工作委員會聯合組織研製的漢字使用規範，自2001年開始研製，原定名《規範漢字表》。該字表整合了《第一批異體字整理表》（1955年）、《簡化字總表》（1964年初發表，最後修訂於1986年）、《現代漢語常用字表》（1988年）以及《現代漢語通用字表》（1988年），並根據中國大陸用字現狀加以修補和完善。歷八年研製，於2009年8月12日放出徵求意見稿，於2013年6月5日正式頒佈，成為社會一般應用領域的漢字規範，原有相關字表從即日起停止使用。

字表共收字8105個，一級字表為常用字集，收字3500個，主要滿足基礎教育和文化普及的基本用字需要。二級字表收字3000個，使用度僅次於一級字。一、二級字表合計6500字，主要滿足出版印刷、辭書編纂和信息處理等方面的一般用字需要。三級字表收字1605個，是姓氏人名、地名、科學技術術語和中小學語文教材文言文用字中未進入一、二級字表的較通用的字，主要滿足信息化時代與大眾生活密切相關的專門領域的用字需要。

### 資料架構

[han-WordCharacter.json](Data/han-WordCharacter.json)

``` json
{
    "serial": "0001",
    "word": "一",
    "bopomofo": "ㄧ"
}
```

- 共三個陣列，分別存放三級字表

### 資料來源

[通用规范汉字表](https://zh.wikisource.org/wiki/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83%E6%B1%89%E5%AD%97%E8%A1%A8)

## 相關文件

- [Wiki: 漢字標準列表](https://zh.wikipedia.org/zh-tw/%E6%BC%A2%E5%AD%97%E6%A8%99%E6%BA%96%E5%88%97%E8%A1%A8)