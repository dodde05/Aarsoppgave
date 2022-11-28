#!/bin/bash

# Update package manager
apt update

# Basic server setup
name=$1

echo "Oppsett for bruker $name"
adduser $name
usermod -aG sudo pygame

apt install ufw -y
apt install openssh-server

ufw allow OpenSSH
ufw enable

# Installing LAMP stcak
apt install apache2 -y
apt install mariadb-server -y
apt install php libapache2-mod-php php-mysql -y

ufw allow in "WWW Full"
ufw allow 3306

# Installing phpmyadmin
apt install php-mbstring php-zip php-gd -y

# Kommandoer med brukerinput
mysql_secure_installation
apt install phpmyadmin -y