#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/ai/alien-supervisor:latest ..
docker push trojanctf2025challenges.azurecr.io/ai/alien-supervisor:latest
