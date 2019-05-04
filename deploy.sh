#!/bin/bash
# Deploy the frontend

# copy the folder
cp -r ./frontend/* /var/www/frontend

# restart the service
sudo systemctl restart frontend