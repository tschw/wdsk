#!/bin/sh

OUTPUT_DIRECTORY='for_your_server'

if test -z "$1" ; then
	echo "Please specify the hostname of your server." >&2
	exit 1
fi

cd `dirname $0`

mkdir -p "${OUTPUT_DIRECTORY}"
chmod go-rx "${OUTPUT_DIRECTORY}"
cd "${OUTPUT_DIRECTORY}"

rm -f $1.key $1.csr $1.crt $1.conf

# Create key:
openssl genrsa -out $1.key 2048
set -x
# Request certificate request:
cat >$1.conf <<EOF
[ req ]
default_bits           = 2048
prompt                 = no
default_md             = sha256
distinguished_name     = req_distinguished_name
req_extensions         = x509v3_FQDN

[ req_distinguished_name ]
countryName            = DE
stateOrProvinceName    = Berlin
localityName           = Berlin
organizationName       = Me, myself and I
organizationalUnitName = Software Development
commonName             = $1

[ x509v3_FQDN ]
keyUsage               = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName         = DNS:$1
EOF

openssl req -new -config $1.conf -key $1.key -out $1.csr

# Service the request:
openssl x509 -req -extfile $1.conf -extensions x509v3_FQDN -in $1.csr -CA ../for_your_browser/myCA.pem -CAkey ../myCA.key -CAcreateserial -out $1.crt -CAserial ../myCA.srl -days 10000 -sha256

