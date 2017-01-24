#!/bin/bash

apt-get install python3 python3-pip nginx

mkdir /etc/nginx/ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt

pip3 install -r configs/requirements.txt

cp /etc/nginx/sites-enabled/default nginx.default.bak
mv configs/nginx.conf /etc/nginx/sites-enabled/default

# Need to run this not as root
# sqlite3 data.db < schema.sql

service nginx restart
