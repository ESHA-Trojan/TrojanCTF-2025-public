#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/ai/alien-leader:latest ..
docker push trojanctf2025challenges.azurecr.io/ai/alien-leader:latest
