# BASE ITEM STOCK CHECKER

BASEで売り切れをメールで通知するアプリ

最初に売り切れが発生すると、DBに記録され、最初の一回だけ通知
商品を補充すると、リセットされます。

取得するタイミングはCRONを使用します。


# Requirement

* python 3.*
* BeautifulSoup4
* dotenv
* sqlite3

# Installation
任意のエディターで.env.sampleに環境設定を記入し、.envにリネームしてください。

```
$ pip install dotenv beautifulsoup dotenv sqlite3
$ git clone https://github.com/quwahiro/BaseItemStockChecker.git
$ cd base_item_stock_checker
$ vim .env.sample
$ mv .env.sample .env
$ python main.py
```

# Usage
## テストする場合は、topページをtest.htmlとして保存し、main.pyを以下のようにしてください。

```
    filename = 'test.html'
    with open(filename+'.html') as myfile:          
         soup = BeautifulSoup(myfile, 'html.parser')
    
    #res = requests.get(os.environ['URL'])
    #soup = BeautifulSoup(res.text, 'html.parser')

```


## CRONは24時間に1回,12時間に1回程度を推奨します。

```
$ crontab -e
0 1,13 * * * python /PATH/main.py
```

# License

"BASE ITEM STOCK CHECKER" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
