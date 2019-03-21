FROM postgres
ENV POSTGRES_DB lunchnlearndb
ENV POSTGRES_USERNAME postgres
ENV POSTGRES_PASSWORD password
COPY database-schema /docker-entrypoint-initdb.d/