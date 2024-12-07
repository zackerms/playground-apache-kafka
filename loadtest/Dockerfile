FROM alpine:latest

# apache-tools(ab)のインストール
RUN apk add --no-cache apache2-utils

WORKDIR /loadtest

# テストスクリプトとデータをコピー
COPY test.json .

ENV REQUESTS=1000 \
    CONCURRENCY=50

# コンテナ起動時にテストを実行
ENTRYPOINT ab -n ${REQUESTS} \
              -c ${CONCURRENCY} \
              -p test.json \
              -T application/json \
              -k \
              -r \
              ${TARGET_URL}