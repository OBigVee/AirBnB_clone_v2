#!/usr/bin/env bash
# script install and setup nginx web servers for the deployment of web_static

if [ "$(id -u)" -ne 0 ]; then
    echo "Run the script with sudo or as root."
    exit 1
fi

# update server's repository and install nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    apt-get update
    apt-get -y install nginx
fi

# create necessary directories if they don't exist
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

cat << EOF | sudo tee /data/web_static/releases/test/index.html
<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
EOF

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

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
