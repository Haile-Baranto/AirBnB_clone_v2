#!/usr/bin/env bash
# Set up web servers for the deployment of web_static

# Install Nginx if it not already installed
if ! command -v nginx &> /dev/null
then
    # Install Nginx if it not already installed
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create the folder /data/ if it doesn’t already exist
sudo mkdir -p /data/

# Create the folder /data/web_static/ if it doesn’t already exist
sudo mkdir -p /data/web_static/

# Create the folder /data/web_static/releases/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/

# Create the folder /data/web_static/shared/ if it doesn’t already exist
sudo mkdir -p /data/web_static/shared/

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
echo "<html>
  <head>
  </head>
  <body>
    <h1>Test</h1>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://fullstackexpert.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
# Use alias inside your Nginx configuration
sudo sed -i "s@^\tlocation / {@\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n\n\tlocation / {@g" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
