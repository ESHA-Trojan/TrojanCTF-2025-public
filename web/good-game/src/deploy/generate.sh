#!/bin/sh

name=`basename \`dirname \\\`pwd\\\` \``

if test -f ./$name.zip; then
  rm $name.zip
fi

if test -f ./main; then
  rm main
fi

echo "Building main.go"
go build main.go

echo "Zipping"
zip -r $name.zip Pulumi.yaml main

echo "Done"
