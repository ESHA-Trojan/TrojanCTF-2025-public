#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/misc/broken-auth:latest ..
docker push trojanctf2025challenges.azurecr.io/misc/broken-auth:latest
