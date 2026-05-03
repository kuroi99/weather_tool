# Weather Tool

OpenWeatherMap APIを使った天気情報取得ツールです。

## 機能

- 複数都市の現在の天気を表示
- 5日分の天気予報を表示（3時間ごと）
- 雨の予報がある場合にアラート表示
- 到着時刻を指定して該当時間の天気を表示

## 使用技術

- Python 3.12
- Flask
- requests
- BeautifulSoup4
- python-dotenv

## セットアップ

1. 仮想環境を作成して有効化

```bash
python3 -m venv venv
source venv/bin/activate
```

2. ライブラリをインストール

```bash
pip install -r requirements.txt
```

3. `.env`ファイルを作成してAPIキーを設定

4. アプリを起動

```bash
python3 app.py
```

5. ブラウザで`http://127.0.0.1:5000`にアクセス

## 注意

- `.env`ファイルはGitHubにpushしないでください
- OpenWeatherMapの無料プランは1分60回のAPI制限があります