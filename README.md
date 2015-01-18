# mecab-web-api
[![Circle CI](https://circleci.com/gh/bungoume/mecab-web-api.svg?style=shield)](https://circleci.com/gh/bungoume/mecab-web-api)
[![Coverage Status](https://img.shields.io/coveralls/bungoume/mecab-web-api.svg)](https://coveralls.io/r/bungoume/mecab-web-api)
[![Dependency Status](https://gemnasium.com/bungoume/mecab-web-api.svg)](https://gemnasium.com/bungoume/mecab-web-api)
[![License](http://img.shields.io/:license-MIT-blue.svg)](http://doge.mit-license.org)

MeCabを利用した形態素解析WebAPI

![typography-icon](typography-icon.png)

## Description

## Quick Start
using Docker Hub

```sh
$ sudo docker run -d -p 8000:8000 bungoume/mecab-web-api
```

or build container on yourself

```sh
$ git clone https://github.com/bungoume/mecab-web-api.git
$ sudo docker build -t mecab-web-api mecab-web-api
$ sudo docker run -d -p 8000:8000 mecab-web-api
```

then, access http://localhost:8000/static/demo.html

## HTTP API
### Endpoints
```
GET /text-analysis/v1/parse?sentence=<string>
GET /text-analysis/v1/reading?sentence=<string>
```

### parse API sample
```
GET /text-analysis/v1/parse?sentence=エビフライ
```
Takes a JSON object like this:
```json
{
    items: [
        {
            words: [
                {
                    word_cost: 4235,
                    surface: "エビ",
                    pos_detail1: "一般",
                    pos: "名詞",
                    conjugated_type: "",
                    ime_romaji: "ebi",
                    morpheme: "通常",
                    conjugated_form: "",
                    pos_detail3: "",
                    c_cost: -283,
                    pronunciation: "エビ",
                    baseform: "エビ",
                    reading: "エビ",
                    pos_detail2: "",
                    with_whitespace: false,
                    cost: 3952
                },
                {
                    word_cost: 3742,
                    surface: "フライ",
                    pos_detail1: "一般",
                    pos: "名詞",
                    conjugated_type: "",
                    ime_romaji: "hurai",
                    morpheme: "通常",
                    conjugated_form: "",
                    pos_detail3: "",
                    c_cost: 62,
                    pronunciation: "フライ",
                    baseform: "フライ",
                    reading: "フライ",
                    pos_detail2: "",
                    with_whitespace: false,
                    cost: 3804
                }
            ],
            all: {
                cost: 7756,
                wakati: "エビ フライ",
                length: 5,
                wakati_reading: "エビ フライ",
                normalized: "エビフライ",
                ime_romaji: "ebihurai",
                reading: "エビフライ"
            }
        },
        {
            // second cost analysis result
        },
        // ...
    }
    ],
    input_sentence: "エビフライ"
}
```

### reading API sample

```
GET /text-analysis/v1/parse?sentence=今日は良い天気だ
```

Takes a JSON object like this:

```json
{
    items: [
        {
            ignore_all_romaji: "kiyouhayoitennkita",
            romaji: "kixyouhayoitennkida",
            ignore_kogaki_romaji: "kiyouhayoitennkida",
            ignore_soundmark_romaji: "kixyouhayoitennkita",
            qwerty_romaji: "kixyouhayoitennkida",
            reading: "キョウハヨイテンキダ"
        },
        {
            ignore_all_romaji: "konnnitihayoitennkita",
            romaji: "konnnitihayoitennkida",
            ignore_kogaki_romaji: "konnnitihayoitennkida",
            ignore_soundmark_romaji: "konnnitihayoitennkita",
            qwerty_romaji: "konnnitihayoitennkida",
            reading: "コンニチハヨイテンキダ"
        },
        //...
    ],
    input_sentence: "今日は良い天気だ"
}
```

## Licence

[MIT](http://doge.mit-license.org)


## Author

[bungoume](https://github.com/bungoume)
