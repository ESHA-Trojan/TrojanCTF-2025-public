#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/web/chal3-whitehats:latest ..
docker push trojanctf2025challenges.azurecr.io/web/chal3-whitehats:latest
