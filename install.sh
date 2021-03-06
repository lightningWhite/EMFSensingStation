#!/bin/bash

# This script sets up the Raspberry Pi to have the EMF sensing station start up
# on boot. It also performs all the necessary hardware configuration.

echo ""
echo "This script must be run as root."
echo ""

echo "Copying startEMFStation.sh to /etc/init.d and enabling the EMF station to start on boot..."
cp startEMFStation.sh /etc/init.d/
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
# Add the RTC device to the /etc/modules file
echo "rtc-ds3231" >> /etc/modules
# Delete the last line of the file containing 'exit 0'
sed -i '/exit/d' /etc/rc.local
# Place the following at the end of the file followed by exit 0
# This is what will make the hwclock accessible and sync the Pi's time with the
# time reported by the hwclock when the Pi starts.
printf '/bin/bash -c "echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device"\n/sbin/hwclock -s\nexit 0' >> /etc/rc.local
echo "Ensure that the Real Time Clock's time is set correctly. This should be performed manually."
echo "It can be done with 'sudo hwclock -w' while the clock is connected and the 'date' command reports the correct time."

# Create the data and logs directory with the proper permissions
mkdir -p /home/pi/EMFSensingStation/data /home/pi/EMFSensingStation/logs
chown pi:pi /home/pi/EMFSensingStation/data /home/pi/EMFSensingStation/logs

echo ""
echo "The EMF sensing station has been installed!"
echo "The Raspberry Pi must be restarted for the EMF sensing station to start automatically."
echo ""

