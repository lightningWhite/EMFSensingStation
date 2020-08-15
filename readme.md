# EMF Sensing Station

## Overview

The object of this project is to create an Electromagnetic Frequency sensing and
data logging solution using a Raspberry Pi and the EMF-390 monitor. It will log
the average EMF readings over a period of time along with the time and GPS
latitude and longitude coordinates.

## A Brief User's Guide

Here are some brief points for common use of the EMFSensing Station:

To start the EMFStation and begin logging the EMF and GPS readings, simply power
on the Raspberry Pi with the EMF sensor plugged into one of the USB ports, the
PiHAT securely on the GPIO pins, and an external storage device plugged
into one of the USB drives. When the Pi turns on, it will automatically start
the sensing station and begin logging the readings.

When the Pi turns on, always ensure that the EMF sensor is in vertical mode
showing the RF reading. The device is in the correct mode when you can see that
the main screen is in portrait mode and divided into thirds by three horizontal
lines. The top section should show the time (it's okay if it's the wrong time),
the section below the time should be displaying RF, the next section should show
a power density reading (probably in mW/m^2), and the bottom reading should show
the peak density reading since the device was powered on. If it is not in
vertical mode when it turns on, change it to vertical mode, press and hold the
power button to turn off the device, then press and hold the power button to turn
it back on. Then restart the Raspberry Pi to be sure that correct data collection
will begin. The EMF sensor should start up in the same mode as when it was turned
off in this manner. Having the EMF sensor in vertical mode is required for proper
functionality of the EMF sensing station. For any questions about operating the
EMF sensor, visit this documentation page:

https://www.gqelectronicsllc.com/GQ-EMF-360V2-380V2-390_UserGuide.pdf

When the station turns on, the GPS sensor may take up to nine minutes to get its
first lock on the four satellites required for accurate global positioning. This
first start for the GPS is called its cold start. Until a lock is obtained, the
GPS will report a position of 0.0 latitude and 0.0 longitude. Generally, it will
take less than nine minutes to get a fix, but it depends on the strength of the
GPS signals reaching the device. The GPS sensor, like all GPS sensors, may not
work in-doors. It also may not work very well inside of a vehicle. You can know
that the GPS has a fix and is reporting accurate coordinates when the red light
on the GPS sensor begins flashing about once every second consistently for a
little while.

While the EMFSensing station is running, it will gather readings ever two
seconds and log the average of the readings every 10 seconds. It will be
written to an external storage device if one is plugged in. If one is not
connected to the Pi, the data will be written to the SD card at
`/home/pi/EMFSensingStation/data/<date--time>.csv`. The data file will be named 
as the date and time of when the station was started in the format of
`YYYY-MM-DD--HH-MM-SS.csv`. 

To retrieve the data, the Pi can be powered off and the external storage device
can be disconnected from the Pi. The data can then be transferred to another
computer for analysis. To begin logging again, simply plug the external storage
device back into the Pi and turn the Pi back on following the same steps above.

Additional documentation pertaining to the EMF Sensing station can be found
below.

As a side note, [this website](https://gpspointplotter.com/) can take a series
of latitude and longitude coordinates and plot them on a map. It can be helpful
to visualize the route of a logging session when in motion.

## Hardware

Raspberry Pi 3 Model B Board
* 40 GPIO Pins - [Pinout](https://pinout.xyz/#)

### Sensors

This project is set up to handle the following sensors:

* [EMF-390 Sensor](https://www.amazon.com/Advanced-GQ-Multi-Field-Electromagnetic-Radiation/dp/B07JGJ897T)
  * Provided by GQ Electronics
  * Software for running a command line interface on the Raspberry Pi can be
  downloaded [here](https://gitlab.com/codref/em390cli/-/tags/v0.1.0).
  * [Manual](https://www.gqelectronicsllc.com/GQ-EMF-360V2-380V2-390_UserGuide.pdf)
* [GPS Sensor](https://www.amazon.com/gp/product/B07P8YMVNT/ref=ask_ql_qh_dp_hza?th=1)
  * [Manual](https://drive.google.com/file/d/15cIa03wqNB7sItn6I2s5xZ8PGOZ1Q0JF/view)
  * Another project that uses this sensor can be found [here](https://randomnerdtutorials.com/email-alert-system-on-location-change-with-raspberry-pi-and-gps-module/).

### Misc Parts

* [Adafruit Perma-Proto HAT for Pi Mini Kit - No EEPROM](https://www.adafruit.com/product/2310)
* [5.9 x 4.3 x 2.8inch (150 x 110 x 70mm) Junction Box](https://www.amazon.com/Zulkit-Dustproof-Waterproof-Universal-Electrical/dp/B07PVVDLCC/ref=asc_df_B07Q1YBFLP/?tag=&linkCode=df0&hvadid=344005018279&hvpos=&hvnetw=g&hvrand=4742956269277649464&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9029805&hvtargid=pla-807538012684&ref=&adgrpid=69357499415&th=1)
* [5.9 x 5.9 x 2.8inch (150 x 150 x 70mm) Junction Box](https://www.amazon.com/LeMotech-Dustproof-Waterproof-Electrical-150mmx150mmx70mm/dp/B075DG55KS/ref=sr_1_4?dchild=1&keywords=150x150x70+junction+box+Zulkit&qid=1590254877&sr=8-4)
* [ChronoDot 2.1 (DS3231 Chip) Real Time Clock](https://www.adafruit.com/product/255)


## Raspberry Pi Configuration

This works well with the [NOOBS Raspbian OS](https://www.raspberrypi.org/downloads/noobs/)
installation. This was all tested with the Buster version of Raspbian on a
Raspberry Pi 4.

TODO: Verify if this is needed
In order to use the I2C and SPI interfaces, these have to be enabled. This can
be done by running `sudo raspi-config` and enabling I2C and SPI in the
`Interfacing Options`.

Also, since the GPS module requires serial communication,
this has to be enabled. To do this in `raspi-config`, select Interfacing
Options and then select `Serial`. When it asks "Would you like a login shell to
be accessible over serial?" select "No". Then when it asks "Would you like the
serial port hardware to be enabled?" select "Yes".

A reboot is required for these changes to be fully enabled. This can be done by
running `sudo reboot`.

### Real Time Clock

The Raspberry Pi can't keep accurate time when it's disconnected from the
internet. For this reason, we use a Real Time Clock (RTC) module. We've
chosen to use the ChronoDot 2.1. Note that the `install.sh` script will
configure the Pi to use the Real Time Clock. For completeness, the steps
performed are documented below. **However**, the only step that the `install.sh`
script does not do is set Real Time Clock's time. **This must be done for it
to be accurate.**

The following location provides a nice tutorial for setting up the Raspberry Pi
to use the RTC:

* [Adding a DS3231 Real Time Clock To The Raspberry Pi](https://www.raspberrypi-spy.co.uk/2015/05/adding-a-ds3231-real-time-clock-to-the-raspberry-pi/)

The following instructions come largely from the link above.

Ensure the following connections to the Raspberry Pi 3 Model B:

* GND of the RTC connected to pin 9 (Ground)
* VCC of the RTC connected to pin 17 (3v3 Power)
* SCL of the RTC connected to BCM 3 (SCL)
* SDA of the RTC connected to BCM 2 (SDA)

To view the I2C address of the RTC, the following command can be run:

```
sudo i2cdetect -y 1
```

This may show the addresses of other connected I2C devices, but the RTC address
will likely by 0x68.

The following line needs to be appended to the /etc/modules file:

```
rtc-ds3231
```

In order to synchronize the Raspberry Pi's time with the RTC when the Pi boots,
the following needs to be added to the `/etc/rc.local` file right before the
`exit 0` at the end: 

```
/bin/bash -c "echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device"
/sbin/hwclock -s
```

The Raspberry Pi should then be rebooted:

```
sudo reboot
```

The date and time reported by the Raspberry Pi can be viewed with the `date`
command. If the time needs to be manually set, it can be done with a command
such as the following:

```
sudo date -s "29 AUG 1997 13:00:00"
```

When the time is correctly set, the system date and time can be written to the
RTC module with the following command:

```
sudo hwclock -w
```

The time can then be read from the RTC with this command:

```
sudo hwclock -r
```

To verify that the system time and the RTC time is the same, the following
command can be run:

```
date; sudo hwclock -r
```

To verify that the RTC is correctly keeping time and that the Raspberry Pi
will use it when it boots, power down the Raspberry Pi, disconnect the
power cable, remove the network connection, connect the Pi to a monitor and
keyboard, leave it overnight, and then power it up and use "date" to
verify that the time reported is correct.

## Dependencies and Prerequisites

The project must be cloned to `/home/pi/` for the scripts to work correctly.
This can be done by running the following:

```
git clone https://github.com/lightningWhite/EMFSensingStation.git
```

The project requires Python 3 to be installed. 

Once this repository is cloned, perform the following steps in the repository
directory:

Create a python virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

Install the pip dependencies of the project (Note: Don't use sudo for the pip
installation in the virtual environment): 

```
pip3 install -r requirements.txt
```

Install `tmux`:

```
sudo apt-get update
sudo apt-get install tmux
```

The `install.sh` script when run will copy the necessary files to `/etc/init.d`
so the EMF station will start on boot automatically. It will also create a
mount point and modify the fstab so an external USB storage device will be
automatically mounted on boot. It will also configure the Pi to automatically
connect to a network named `EMF` if present. This can be helpful if you want
to connect to the Pi wirelessly using a mobile hotspot. The script will also
configure the Pi to use the Real Time Clock for time. This script must be run
as root and the Pi must be restarted for the changes to take effect:

```
sudo ./install.sh
sudo reboot
```

## Running the EMF Sensing Station

The `startEMFStation.sh` script will start a tmux session and call the
`initializeEMFStation.sh` script. This script will source the python virtual
environment. It will then start the EMF station and detach the tmux session. 
This makes it so the ssh session can time out or be terminated and the EMF
station process will remain running. Using tmux also allows the user to attach
to the session at any time and view the real-time output of the program.

After the `startEMFStation.sh` script has been executed (this must be run with
sudo for it to access /dev/serial0 where the GPS data is streamed: 
sudo ./startEMFStation.sh), you can attach to the process and view the output
in real-time by typing `tmux attach`. To detach from the session again so it
can continue running when the ssh session times out or you log out from it,
type `Ctrl+b` and then `d`. This will put it in the background to continue
running.

Note that when the EMF station has been started automatically on boot,
to view the real-time output of the EMF station, you must attach to the
tmux session as root: `sudo tmux attach`.

The EMF-390 sensor must be connected to the Raspberry Pi via USB for the
station to start up correctly. The sensor must also be in vertical mode viewing
RF. If this is not set up like this, the EMF Station may crash and/or won't
report the correct EMF values. Also, it's important that the battery is
removed from the EMF-390 device. Some resources on the internet report that
the charging circuit is not shielded. Since it is plugged into the Raspberry
Pi, this unshielded circuit would throw off the EMF readings.

When the sensing station is started with the `startEMFStation.sh` script, the
real-time output will be written to a log file by the name of the time the
EMF station was started and be written to the /logs directory in the repository.
Log messages are written to stdout and should capture most of the problems that
may arise while the EMF sensing station is running. This can assist in
debugging.

Note that a cold start of the GPS (when it first starts up) may require several
minutes before valid GPS coordinates are obtained.

## Data Logging

As the EMF station runs, it will log readings from the EMF sensor and GPS
sensor at a configurable rate. This can be set in the emf_station.py file. The
LOG_INTERVAL defines how often the readings will be logged. The
ACCUMULATION_INTERVAL defines how often samples should be taken of the EMF
sensor in order to calculate and averages or maximums. The
ACCUMULATION_INTERVAL should be less than the LOG_INTERVAL.

A data file will be created every time the EMF station is started and it
will be saved to `/home/pi/EMFSensingStation/data` and be named the date and time
of when it was created.

The CSV file will grow at a rate of around 4 Kilobytes for every 13 entries.

If an external USB storage device is connected, such as a thumbdrive, the data
file will be copied to it after each data record is written. When the next
record is to be copied to the external storage drive, the previously copied
file will have its name changed to have a .bak extension so it isn't overwritten
until the latest copy of the data file is obtained. The next time the data file
is to be copied to the external storage device, the .bak file will be
overwritten with the previously backed up file and the new data file will be
copied to the drive.

Here is some sample data that was logged by the station:

```
Record Number, Time, Avg. RF Watts (W), Avg. RF Watts Frequency (MHz), Peak RF Watts (W), Frequency of RF Watts Peak (MHz), Peak RF Watts Frequency (MHz), Watts of RF Watts Frequency Peak (W), Avg. RF Density (W m^(-2)), Avg. RF Density Frequency (MHz), Peak RF Density (W m^(-2)), Frequency of RF Density Peak (MHz), Peak RF Density Frequency (MHz), Density of RF Density Frequency Peak (W m^(-2)), Avg. Total Density (W m^(-2)), Max Total Density (W m^(-2)), Avg. EF (V/m), Max EF (V/m), Avg. EMF (mG), Max EMF (mG)
1, 2020-05-16 16:38:54.100572, 0.0000000003326912, 694.0, 0.0000000050000000, 1866.0, 1866.0, 0.0000000050000000, 0.0000338235294118, 732.6, 0.0005000000000000, 1866.0, 1881.0, 0.0003000000000000, 0.0001264705882353, 0.0010000000000000, 693.7, 886.0, 1.2, 1.4
2, 2020-05-16 16:53:55.786168, 0.0000000008500571, 759.1, 0.0000000250000000, 1880.0, 1881.0, 0.0000000040000000, 0.0000542857142857, 776.4, 0.0013000000000000, 1880.0, 1881.0, 0.0004000000000000, 0.0003014285714286, 0.0011000000000000, 676.6, 844.0, 1.3, 1.5
3, 2020-05-16 17:08:56.629817, 0.0000000004531143, 741.0, 0.0000000050000000, 1861.0, 1878.0, 0.0000000030000000, 0.0000285714285714, 758.6, 0.0005000000000000, 1861.0, 1878.0, 0.0003000000000000, 0.0002600000000000, 0.0011000000000000, 690.1, 889.6, 1.2, 1.4
4, 2020-05-16 17:23:58.887251, 0.0000000005634000, 775.9, 0.0000000160000000, 1884.0, 1884.0, 0.0000000160000000, 0.0000028571428571, 671.5, 0.0001000000000000, 1880.0, 1880.0, 0.0001000000000000, 0.0004728571428571, 0.0028000000000000, 664.1, 880.0, 1.2, 1.5
5, 2020-05-16 17:38:59.409071, 0.0000000002303000, 670.8, 0.0000000030000000, 1872.0, 1872.0, 0.0000000030000000, 0.0000228571428571, 776.0, 0.0003000000000000, 1872.0, 1879.0, 0.0003000000000000, 0.0011057142857143, 0.0029000000000000, 675.8, 880.0, 1.2, 1.4
```

This can easily be viewed by opening the .csv file with a spreadsheet
application such as Microsoft Excel, LibreOffice Calc, or Google Sheets.

## Logging

The `emf_station.py` file initializes a logger. Log messages from the
EMF sensing station will be stored in the `logs` directory by
the same time name as the data file. This log output can be very helpful for
debugging if any issues arise.

## Helpful Connection Information

In order to connect to the Raspberry Pi via ssh, it must be enabled first.
This resource provides some instructions on how to do that:

* https://www.raspberrypi.org/documentation/remote-access/ssh/

One of the methods mentioned is to have the Pi connected to a keyboard and
monitor and then run the following:

```
sudo systemctl enable ssh
sudo systemctl start ssh
```

Note that this can also be done using `raspi-config`.

A helpful tool for finding the IP address of the Raspberry Pi in order to
ssh to it, is `arp-scan`. It can be installed by running the following:

```
sudo apt-get install arp-scan
```

To list the IP addresses of devices on the network, run the following:

```
sudo arp-scan -l
```

### Connecting to the Raspberry Pi Using an Android Phone

#### termux

An Android app called `termux` can be installed from Google Play. This
app provides a terminal on the Android phone. Using this terminal, files
can be copied from the Raspberry Pi via `scp`. Connections can also be made to
the Pi using `ssh`. To do this, open termux on an Android phone and run the
following commands:

Enable tmux to access the phone's storage so you can access any copied files
from the Pi:

```
termux-setup-storage
```

Allow access when the dialog pops up.

Install ssh and scp:

```
pkg install openssh
```

You can now ssh to the Raspberry Pi using the Pi's IP address if you're on
the same network (192.168.0.23 as an example Pi IP address):

```
ssh pi@192.168.0.23
```

You can also copy one of the data files from the Pi to your phone with a
command such as this:

```
cd storage/downloads
scp pi@192.168.0.23:/home/pi/EMFSensingStation/data/05-07-2020--19-08-22.csv .
```

Enter the Raspberry Pi's password and the file should be copied to the phone.

The file should then be copied to the Downloads folder of the phone.

If you want to copy all of the data files to your phone, you can do so using
scp like this:

```
cd storage/downloads
scp -r pi@192.168.0.23:/home/pi/EMFSensingStation/data/ .
```

#### VNC Viewer - Remote Desktop

`VNC Viewer - Remote Desktop` can be installed via Google Play. Once this is
installed, a vncserver can be started on the Raspberry Pi. vncserver needs to
be enabled on the Pi before doing this. This can be done by running
`raspi-config` and selecting `Interfacing Options`. Then select VNC and
enable it.

Once it is enabled, a vncserver can be started by running the following:

```
vncserver :1
```

This will start the vncserver on port 5901.

Using the Android vnc client application, you can connect to the Pi by
entering the IP address of the Raspberry Pi followed by a :1 such as this:

```
192.168.0.23:1
```

This will provide the desktop GUI with which you can interact.

#### Connecting Using a WiFi Hotspot from an Android Phone

Since the Pi will likely be running in a location without WiFi, in order to
connect via the methods above, some sort of network needs to be in place. This
can be a mobile hotspot.

The Raspberry Pi can be configured to connect automatically to a WiFi hotspot.
Then the mobile device or another device connected to the same network can
ssh to the Pi or scp files from the Pi to the phone. Do the following to make
this possible:

Modify the `wpa_supplicant.conf` file located at `/etc/wpa_supplicant/` to
include the hotspot network and password. An example of what should be added
is as follows:

```
network={
  ssid="EMFNetwork"
  psk="password"
  key_mgmt=WPA-PSK
  priority=20
}
```

The Raspberry Pi must be restarted for the changes to take effect.

This will cause the Raspberry Pi to automatically connect to a network with the
name of "EMFNetwork" and use the password "password" if the network is
present. Setting the priority to 20 (some arbitrarily large number) should
ensure that it will be the first network that it will try to connect to. Note
that the `install.sh` script will configure this network connection when it is
run.

On the mobile device, set up a hotspot with that name and password and turn it
on. The Pi should automatically connect to the hotspot.

The mobile hotspot should show that one device is connected. To view the IP
address of the Raspberry Pi, open up a terminal in the phone using something
like Termux and type the following:

```
ip neigh
```

This should show the IP address of the Raspberry Pi on the hotspot network.

Any of the previously mentioned methods should now work to connect to the
Raspberry Pi using the mobile device.

## Files

The following files are the primary files used in the EMF sensing station:

* emf_station.py - The main program loop
* emf.py - EMF sensing

The following files are used for setting up and running the EMF sensing station:

* install.sh - Configures the Raspberry Pi to start the EMF station on boot
* initializeEMFStation.sh - Sources the Python3 virtual environment
* startEMFStation.sh - Starts the EMF sensing station in a tmux session and
runs it in the background

### Primary EMF Sensing Files 

#### emf_station.py

This file contains the main program loop. It contains all the code for the
EMF sensing station with the exception of the following files, which are
imported:

* emf.py

As the EMF sensing station runs, it will gather and log readings from the
sensors at a configurable rate. The LOG_INTERVAL defines how often the readings
will be logged. The ACCUMULATION_INTERVAL defines how often samples should be
taken of some of the sensors in order to calculate and averages or maximums.
The ACCUMULATION_INTERVAL should be less than the LOG_INTERVAL.

#### gps.py

This file is written to interface with the GT-U7 module to obtain GPS
information. The information of interest for this application is the
GPGGA NMEA data. This consists of the following fields:

* GPGGA - the message type
* timestamp - UTC time in hours, minutes, and seconds
* latitude - in DDMM.MMMMM format. Decimal places are variable
* latitude direction
* longitude - in DDMM.MMMMM format
* longitude direction
* fix quality
* number of satellites used in the coordinate
* horizontal dilution of precision
* altitude of the antenna
* units of altitude
* height of geoid above WGS84 ellipsoid
* units used by the geoid separation
* age of the correction (if any)
* correction station id (if any)
* checksum

The gps.py file has a function named `get_latitude_longitude()` that reads the
GPS string and parses out the latitude and longitude from it. Those values
are then returned.

Ensure the following connections:

* GND of the GPS sensor to GND on the Pi
* VCC of the GPS sensor to 3v3 on the Pi
* RX of the GPS sensor to BCM 14 (TX) on the Pi
* TX of the GPS sensor to BCM 15 (RX) on the Pi

Also ensure that serial is enabled on the Pi.

#### logging.py

This file provides logging functionality. A path to the log file location is
passed to the intialize_logger function and then messages can then be logged
by calling the log function and passing a message. The message will be logged
with the current time.

#### EMF-390 Sensor

A command line interface tool has been written that allows the Raspberry Pi
to perform real-time logging of the readings from the EMF-390 sensor. This
tool was written by Davide Dal Farra.

The application can be downloaded from [here](https://gitlab.com/codref/em390cli/-/tags/v0.1.0).
Simply download the Arm Linux zip file to the Raspberry Pi and unzip it:

`unzip emf390cli.zip`

A forum that may be helpful that references this application and source code 
can be found [here](https://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=6308).

Instructions for running the tool can be found in the project's README
[here](https://gitlab.com/codref/em390cli/-/blob/master/README.md).

As a precaution in case the project disappears, the source code for it has been
added to this repository. The clone of the GitLab project also includes the
build directory with the application binaries for different platforms.
However, as long as the project is alive, it will be best to use the provided
application in order to receive the updates. The source code is licensed under
the GNU General Public License. Instructions for building from source on the
Raspberry Pi are provided in the README file.

The README of the project also notes that to use the device for real-time data
logging, it's best to remove the battery. It says that the charging circuit is
not shielded and it will produce a lot of interference.

To read data in real-time from the device in a CSV format, the following command
can be used:

```
emf390cli -p /dev/ttyUSB0 -f '%w%d%e%t%k%E%M' --csv
```

This specifies the serial port to connect to, the desired format, and to export
the fetched values as a CSV string.

The following is some sample output:

```
rfwatts, 0.000000000158, 158, pW, 672, MHz
rfdbm, -68, -68, dbm, 672, MHz
rfdensity, 0.0001, 0.1, mW/m2, 672, MHz
rftotaldensity, 0.06720000000000001, 67.2, mW/m2, 0, n/a
rftotaldensitypeak, 0.6354, 635.4, mW/m2, 0, n/a
ef, 11.8, 11.8, V/m, 0, n/a
emf, 0.6, 0.6, mG, 0, n/a
```

For each metric, it lists the name, the value, the raw value, the raw value
unit, the MHz, and the MHz unit.

IMPORTANT: In order for the correct values to be obtained, the EMF sensor must
be in `Vertical Mode` or else the readings will be incorrect and a potential
crash could occur.

Some additional notes:
 
rfwatts and rfdbm are different forms of the same number. The problem is that it
appears that they are calculated sequentially. This means that the readings of
the sensor may be different for each reading reported in the output. This is not
ideal. They should not contradict each other. One or the other reading could be
taken and then converted to the other form if it's desirable to have both.

I'm not sure what equation is being used for calculating the power density.
According to [Wikipedia](https://en.wikipedia.org/wiki/Surface_power_density),
the equation for surface power density is the following:

```
Pd (Watts/meter^2) = E x H (Volts/meter x Amperes/meter)
```

And at far field, the ratio between E and H becomes a fixed constant of 377
ohms, making the following two equations applicable as well:

```
Pd = H^2 x 377 Ohms
Pd = E^2 / 377 Ohms
```

However, using these equations and the readings from the sensor don't seem to
calculate the power density reported by the sensor. After asking about this on
the forum, the supplier indicated that the value is simply reported by the
sensor, rather than using a formula to calculate it.

Additionally, in radar applications, there is a power density equation that is as
follows, according to this
[website](https://www.pasternack.com/t-calculator-power-density.aspx):

```
Power Density = (Pout * Gain) / (4 * PI * Distance^2)
```

The gain used by the EMF-390 sensor for the antennae is 10 (configurable in the
sensor settings, but the forum recommends to leave it at 10 unless using some
sort of external antenna). The distance can be calculated when D when a Power
Density is reported, however, this distance seems to change for different
readings, so it's unclear what's being used for the distance in the equation.
Pout is probably the rfwatts reading.

Since the gain and the distance (probably) is hard-coded, the power density is
not the value of a tower or something. It is just a relative value at the
current location.

It's unclear how total power density is being calculated. It might be some sort
of sum.

This forum is helpful and may be a good resource for clearing up some of the
questions mentioned above: https://www.gqelectronicsllc.com/forum/forum.asp?FORUM_ID=18

Although there are some discrepancies between the values obtained from the
emf390cli tool, these discrepancies are mitigated in the `emf_station.py`
file by collecting values and then reporting averages and maximums rather than
simply reporting each of the values directly reported by the tool.

IMPORTANT: When the EMF-390 sensor is plugged into the Raspberry Pi, the EF
values are extremely high. It's unknown why this happens when it's plugged
into the Raspberry Pi. It doesn't report high values when just the battery
is in use or when it's plugged into computers besides the Raspberry Pi.

### Board Assembly Notes

Remember to turn off the Pi before taking off or putting on the Pi HAT board.
Sometimes bugs can crop up by leaving the Pi on while doing this that can take
a good while to figure out.

* Solder the GPS module to the Pi-HAT. It's best if the antenna is strung
outside of the waterproof junction box for better receptivity.
* Connect the Real Time Clock. Remember to test it out and set the clock. Again,
make sure you have the Pi off and start it after it's connected. Also, remember
to follow the set up instructions near the top of this readme to configure and 
set the Real Time Clock.
* Use the pin connections defined in this readme and in the source files for
how everything should be connected.
