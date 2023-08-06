# JIS X 0402

このライブラリはJIS X 0402で規定されている全国地方公共団体コードを扱うライブラリです。

参照しているデータは[総務省のホームページ](https://www.soumu.go.jp/denshijiti/code.html)からダウンロードしたものです。

## Installation

```sh
pip install jisx0402
```

## Usage

### Recordクラス

データはこのRecordクラスのインスタンス単位で扱います。
このクラスはフィールドとして下記を持っています。

- 全国地方公共団体コード
- 都道府県名
- 都道府県名(半角カナ)
- 市町村名
- 市町村名(半角カナ)

#### 例

```py
Record(code="010006", prefecture="北海道", prefecture_kana="ﾎｯｶｲﾄﾞｳ", city="", city_kana="")

Record(code="011002", prefecture="北海道", prefecture_kana="ﾎｯｶｲﾄﾞｳ", city="札幌市", city_kana="ｻｯﾎﾟﾛｼ")

```

### code2name

全国地方公共団体コード -> Recordの変換を行います。

#### 例

```py
>>> code2name("010006")
Record(code="010006", prefecture="北海道", prefecture_kana="ﾎｯｶｲﾄﾞｳ", city="", city_kana="")
```

### search

フィールド名と正規表現を用いてRecordの検索を行います。

#### 例

```py
>>> search("full_city_name", r"福.県$")
[
    Record(code='070009', prefecture='福島県', prefecture_kana='ﾌｸｼﾏｹﾝ', city='', city_kana=''),
    Record(code='180009', prefecture='福井県', prefecture_kana='ﾌｸｲｹﾝ', city='', city_kana=''),
    Record(code='400009', prefecture='福岡県', prefecture_kana='ﾌｸｵｶｹﾝ', city='', city_kana='')
]
```
