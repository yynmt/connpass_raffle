# connpass raffle

- connpassから取得したcsvファイルを利用した抽選Webアプリ

## Dockerを使用しての起動方法
Docker環境で起動する場合は以下の手順で起動できます。
```
docker build -t connpass_raffle .
docker run -p 8080:5000 connpass_raffle
```
`[起動しているホストのIPアドレス]:8080`(例:`127.0.0.1:8080`)にWebブラウザからアクセスしてください。