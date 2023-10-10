#!/bin/bash

# Prompt for username (default: admin)
read -p "Enter the username (default: admin): " username
username=${username:-admin}

# Prompt for password (default: admin)
read -p "Enter the password (default: admin): " password
password=${password:-admin}

# Prompt for host (default: 0.0.0.0)
read -p "Enter the host (default: 0.0.0.0): " host
host=${host:-0.0.0.0}

# Prompt for port (default: 8833)
read -p "Enter the port (default: 8833): " port
port=${port:-8833}

# Run as user (default: root)
read -p "Enter the user to run as (default: root): " user
user=${user:-root}

# Generate systemd service file
service_file="[Unit]
Description=IMGBKP - Self-Hosted Image and Video Hosting App
After=network.target

[Service]
ExecStart=/usr/bin/python3 $(pwd)/imgbkp.py --username $username --password $password --host $host --port $port
WorkingDirectory=$(pwd)
Restart=always
User=$user

[Install]
WantedBy=multi-user.target
"
echo "$service_file" > imgbkp.service

# Ask to copy service file to systemd directory
read -p "Do you want to copy the service file to systemd directory? (y/n): " copy_service
if [ "$copy_service" == "y" ]; then
    sudo cp imgbkp.service /etc/systemd/system/
    sudo systemctl daemon-reload
    echo "Service file copied to systemd directory."
fi

# Ask to enable the service
read -p "Do you want to enable the service in systemd? (y/n): " enable_service
if [ "$enable_service" == "y" ]; then
    sudo systemctl enable imgbkp.service
    echo "Service enabled in systemd."
fi

# Ask to start the service
read -p "Do you want to start the service now? (y/n): " start_service
if [ "$start_service" == "y" ]; then
    sudo systemctl start imgbkp.service
    echo "Service started."
fi

echo "Setup completed."
