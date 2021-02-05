#docker build -t sanare-http-log:latest .
#docker run -it -p 5432:5432 --network sanare-py_sanare sanare-http-log
FROM postgres:9.3

ENV POSTGRES_USER sanare
ENV POSTGRES_PASSWORD sanare
ENV POSTGRES_DB sanare_http_log
ADD CreateDB.sql /docker-entrypoint-initdb.d/