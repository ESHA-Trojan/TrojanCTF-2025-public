#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/web/forum-track-blockchain:latest ../blockchain
docker push trojanctf2025challenges.azurecr.io/web/forum-track-blockchain:latest

docker build -t trojanctf2025challenges.azurecr.io/web/forum-track-server:latest ../server
docker push trojanctf2025challenges.azurecr.io/web/forum-track-server:latest

docker build -t trojanctf2025challenges.azurecr.io/web/forum-track-client:latest ../client
docker push trojanctf2025challenges.azurecr.io/web/forum-track-client:latest
