#!/usr/bin/env bash

TAG="lnlpostgres"
docker rm -f "$TAG"
docker build . -t "$TAG"
docker run -d --name "$TAG" -p 5432:5432 "$TAG"