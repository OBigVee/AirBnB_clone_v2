#!/usr/bin/env bash
# script install and setup nginx web servers for the deployment of web_static

# update server's repository and install nginx if not already installed
apt-get update
apt-get -y install nginx

# create necessary directories if they don't exist
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# create test html file
cat << EOF | sudo tee /data/web_static/releases/test/index.html
<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
EOF

# create a symbolic linking to release/test/ dir
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the current user
chown -R ubuntu:ubuntu /data/

# set up nginx 
SERVER=$(hostname)

SERVER_CONFIG="server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
            add_header X-Served-By '$SERVER';
            try_files \$uri \$uri/ =404;
    }

    location /hbnb_static {
        add_header X-Served-By '$SERVER';
        alias /data/web_static/current;
    }
}"
echo -e "$SERVER_CONFIG" > /etc/nginx/sites-available/default
systemctl restart nginx

exit 0
