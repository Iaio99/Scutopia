#!/bin/sh
ip=$(wget -q -O - ipinfo.io/ip)
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem $ip 
