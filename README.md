## 概要
FigmaのAPIを叩いてユーザーごとのデータを集計する

## 使い方
* clone
```
git clone git@github.com:kilisima/FigmaApi.git
```
* pip install
```
pip install < requirements.txt
```
* figma personal token を取得 \
[personal access token](https://www.figma.com/developers/api#access-tokens)
* AccessTokenを`.env`に設定
```
touch .env
echo "FIGMA_TOKEN=${ACCESS_TOKEN}" > .env
```
* `teams.yaml`を作成
```Shell
touch teams.yaml
```
内容
```YAML
team_id:
  - 1155843800622215436
```
* 実行
```
python main.py
```
* `data.db`が生成される
```
ls -lrta data.db
-rw-r--r--  1 staff  staff  8192 Oct  2 14:34 data.db
```

## データを参照する
SQLITE3のサイトを記述するが、3rdパーティのソフトウェアなどでも参照できる
* sqlite3をインストール
[sqlite3](https://www.sqlite.org/download.html)
* sqlite3で開く
```
sqlite3 data.db
```
* 内容を確認
```
select * from figmadata;
```


## LICENSE
Apache License 2.0 \
[LICENSE](LICENSE)
