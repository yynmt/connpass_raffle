# connpass raffle
connpassから取得したcsvファイルを利用した抽選Webアプリ

## 事前準備
以下のファイルを用意する必要があります。 connpass_raffle ディレクトリ以下に用意してください。
- part.csv - 全抽選対象者を列挙した csv ファイル
- item.csv - 抽選対象景品を列挙した csv ファイル

## 実行環境
miniconda にて同梱の `conda_env.yaml` を使って環境を構築してください。`tenkey_raffle` という名前の環境が作成されます。
```
conda env create -f=conda_env.yml
```

## 実行手順
前述で作った環境をアクティブにしてください。
```
conda activate tenkey_raffle
```
`main.py` を Python で実行してください。
```
python main.py
```
最後に `127.0.0.1:5000` に Web ブラウザからアクセスしてください。
