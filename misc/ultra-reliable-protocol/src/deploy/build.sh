#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/misc/typed-proto:latest ..
docker push trojanctf2025challenges.azurecr.io/misc/typed-proto:latest
