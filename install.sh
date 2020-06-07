#!/bin/bash

# This script sets up the Raspberry Pi to have the EMF sensing station start up
# on boot.

echo ""
echo "This script must be run as root."
echo ""

echo "Copying startEMFStation.sh to /etc/init.d"
cp startEMFStation.sh /etc/init.d/

echo "Enabling the EMF station to start on boot"
update-rc.d startEMFStation.sh defaults

echo "Creating /mnt/usb1 as a mount point for an external storage device..."
mkdir -p /mnt/usb1
sudo chown -R pi:pi /mnt/usb1

echo "Modifying the fstab to mount an external USB storage device to /mnt/usb1..."
echo "/dev/sda1 /mnt/usb1 vfat uid=pi,gid=pi,umask=0022,sync,auto,nofail,nosuid,rw,nouser 0 0" >> /etc/fstab

# TODO: Change the default network to EMF or something
echo "Setting up a default network to which the Pi should attempt to connect if present..."
printf 'network={\n\tssid="Weather"\n\tpsk="weatherStationNetwork"\n\tkey_mgmt=WPA-PSK\n\tpriority=20\n}\n' >> /etc/wpa_supplicant/wpa_supplicant.conf

echo "Configuring the Pi to synchronize with the Real Time Clock..."
# Delete the last line of the file containing 'exit 0'
sed -i '/exit/d' /etc/rc.local
# Place the following at the end of the file followed by exit 0
printf 'echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device\nhwclock -s\nexit 0' >> /etc/rc.local

echo "Configuring the Pi for the GPS sensor:"
# https://raspberrypi.stackexchange.com/questions/104403/configuration-uart-on-pi-4
# I don't think I want to do the stuff below. I think it messes up the Pi.

#echo ""
#echo "Disabling Bluetooth and enabling UART"
#echo "" >> /boot/config.txt
#echo "dtparam=spi=on" >> /boot/config.txt
#echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt
#echo "force_turbo=1" >> /boot/config.txt
#echo "core_freq=250" >> /boot/config.txt
#echo "enable_uart=1" >> /boot/config.txt
#
## TODO: Find out what this line needs to be. Currently it
##       causes the Pi to not be able to start up correctly.
##echo "dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles" > /boot/cmdline.txt
#
#sudo systemctl stop serial-getty@ttyS0.service
#sudo systemctl disable serial-getty@ttyS0.service
## TODO: This may need to be run after a reboot
##sudo systemctl enable serial-getty@ttyAMA0.service

echo ""

echo "The EMF sensing station has been installed!"
echo "The Raspberry Pi must be restarted for the EMF sensing station to start automatically."
echo ""

