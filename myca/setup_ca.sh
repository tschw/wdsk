#!/bin/sh

cd `dirname $0`

# Create private key
openssl genrsa -des3 -out myCA.key 2048
chmod go-rwx myCA.key

rm -rf for_your_browser
mkdir for_your_browser

# Self-sign it
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 10000 -out for_your_browser/myCA.pem
