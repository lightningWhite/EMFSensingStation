# GPS Sensor
#
# Uses the GT-U7 module to obtain GPS information.
#
# GPGGA NMEA returns the following fields
# GPGGA, time, latitude, longitude, fix quality, number of satellites, horizontal dilution of precision, altitude, height of geoid above WGS84 ellipsoid, time since last DGPS update, DGPS reference station id, checksum
#
# Ensure the following connections:
#  

import serial
import pynmea2
import logger


# Set up the GPS serial port connection
logger.log("Setting up the GPS module serial communication")
port = "/dev/serial0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()


def get_latitude_longitude():
    """
    Obtain and return the current latitude and longitude.
    """

    # Obtain the current location from the GPS sensor
    logger.log("Reading the GPS data") 
    gps_data = ser.readline()
    if gps_data[0:6] == '$GPGGA':
        msg = pynmea2.parse(gps_data)
        latitude = str(msg.latitude)
        longitude = str(msg.longitude)
    
    return latitude, longitude


import time
while True:
    print(get_latitude_longitude())
    time.sleep(1)

