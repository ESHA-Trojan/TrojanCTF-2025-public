#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/pwn/grandpa-ftp-server:latest ..
docker push trojanctf2025challenges.azurecr.io/pwn/grandpa-ftp-server:latest
