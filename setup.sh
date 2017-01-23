#!/bin/bash

apt-get install python3 python3-pip

mkdir /etc/nginx/ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt

pip install -r config/requirements.txt

cp /etc/nginx/sites-enabled/default nginx.default.bak
mv config/nginx.conf /etc/nginx/sites-enabled/default

sqlite3 data.db < schema.sql
