#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/crypto/length-extension:latest ..
docker push trojanctf2025challenges.azurecr.io/crypto/length-extension:latest
