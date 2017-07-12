#!/bin/bash
echo "-------------------------------------------------"
echo " National Instruments RaspberryPi 600x Installer "
echo "-------------------------------------------------"
echo " "
echo "Checking Permissions..."
#Ensure user is root
if [ "$(id -u)" != "0" ]; then
   echo "Error: This Installer must be run as root...exiting" 1>&2
   echo "Try \"sudo sh install.sh\""
   exit 1
fi

echo "Checking System Requirements..."
echo "Updating apt-get..."
apt-get update -qq
echo "Installing lighttpd..."
apt-get install --force-yes lighttpd -qq
echo "Configuring WebServices..."
/etc/init.d/lighttpd stop
touch /var/www/in
touch /var/www/out
touch /var/www/state
echo "Back up origional config file for lighttpd to /etc/lighttpd/lighttpd_orig.conf"
cp /etc/lighttpd/lighttpd.conf  /etc/lighttpd/lighttpd_orig.conf
echo "Configuring Variables..."
cp lighttpd.conf /etc/lighttpd/lighttpd.conf
echo "Installing Files..."
#untar all binaries to /usr/local/bin/natinst/rpi/*
#untar all webservices to /var/www/*
tar xf install_ws.tar -C /
tar xf install_ex.tar -C / 
echo "Starting WebServices..."
/etc/init.d/lighttpd start
echo "Done"
echo " "
echo "Plug in your 600x with NIDAQmxBase Firmware Installed and run"
echo "the examples located at /usr/local/bin/natinst/rpi."

