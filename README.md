# COMIC_BOT
slackに今日発売の漫画情報を出力

## 環境構築
1. リポジトリのclone
    ```
    $ git clone　git@github.com:kyoF/comic-bot.git
    $ cd comic-bot
    ```

2. 環境変数の設定
    ```
    $ touch .env
    ```
    .envファイルに下記を追記
    ```
    incoming_webhook_url={incoming webhookのURL}
    target_scraped_url=https://calendar.gameiroiro.com/kindle-manga.php?year={}&month={}
    ```

3. モジュールの追加
    ```
    $ pip install requests
    $ pip install beautifulsoup4
    $ pip install slackweb
    $ pip install python-dotenv
    ```

4. 実行
   ```
   $ python3 comic.py
   ```

## 実行結果
slackの該当チャンネルに下記が表示されます
```
漫画タイトル
イメージ画像
AmazonURL
出版社
著者
```
