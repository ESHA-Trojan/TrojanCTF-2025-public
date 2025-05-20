#!/bin/sh

set -euxo pipefail

docker build -t trojanctf2025challenges.azurecr.io/pwn/role-based-access:latest ..
docker push trojanctf2025challenges.azurecr.io/pwn/role-based-access:latest
