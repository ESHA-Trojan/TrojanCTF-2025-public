#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/web/nextjs-cve:latest ..
docker push trojanctf2025challenges.azurecr.io/web/nextjs-cve:latest
