#!/bin/bash
# scrip install and setup nginx

if [ "$(id -u)" -ne 0 ]; then
    echo "run script with sudo or as root"
    exit 1
fi

# install nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    apt-get update
    apt-get -y install nginx
fi

# create necessary directories if they don't exist
web_static_dir="/data/web_static"
web_static_releases="$web_static_dir/releases/test"
web_static_shared="$web_static_dir/shared"
web_static_current="$web_static_dir/current"

for dir in "$web_static_dir" "$web_static_releases" "$web_static_shared"; do
    if ! [ -d "$dir" ]; then
        mkdir -p "$dir"
        chown -R ubuntu:ubuntu "$dir"
    fi
done

# create test html file
html_content="<html><head></head><body>Test only</body></html>"
echo "$html_content" > "$web_static_releases/index.html"

# create or update symbolic link
# if [ -L "$web_static_current" ]; then
#     rm -f "$web_static_current"
# fi
ln -sf "$web_static_releases" "$web_static_current"
chown -R ubuntu:ubuntu "/data/"

SERVER=$(hostname)

SERVER_CONFIG="server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name_;

    location / {
            add_header X-Served-By
            try_files \$uri \$uri/ =404;

    }

    location /hbnb_static {
        add_header X-Served-By '$SERVER';
        alias /data/web_static/current;
    }
}"
base -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-available/default"
/etc/init.d/nginx restart

exit 0
# Update Nginx config with alias
# ng_config="/etc/nginx/sites-available/default"
# if ! grep -q "location /hbnb_static" "$nginx_config"; then
#     sed -i '/server_name _;/a \
#     location /hbnb_static/ {\
#         alias /data/web_static/current/;\
#     }' "$ng_config"
#     service nginx restart
# fi

# echo "Web server setup completed!"