#!/bin/bash

if openssl x509 -checkend 2592000 -in yamatsumi.crt; then
  exit
fi

IP_ADDRESS=localhost
SERVER_NAME=$IP_ADDRESS

rm -rf *.key *.csr *.crt

cat <<_MY_CONF_ > yamatsumi.cnf
[ req ]
default_bits = 2048
default_md = sha256
prompt = no
encrypt_key = no
distinguished_name = dn
req_extensions = v3_req

[ dn ]
C = JP
O = $SERVER_NAME
CN = $SERVER_NAME

[ v3_req ]
subjectAltName = @alt_names
extendedKeyUsage = serverAuth

[ alt_names ]
DNS.1 = $IP_ADDRESS

_MY_CONF_

openssl req -new -config yamatsumi.cnf -keyout yamatsumi.key -out yamatsumi.csr
openssl x509 -days 365 -extensions v3_req -req -signkey yamatsumi.key -extensions v3_req -extfile yamatsumi.cnf < yamatsumi.csr > yamatsumi.crt
