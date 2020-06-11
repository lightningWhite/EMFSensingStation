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

# TODO: Remove this when done testing
logger.initialize_logger(f"/home/pi/EMFSensingStation/logs/test.log")

# Set up the GPS serial port connection
logger.log("Setting up the GPS module serial communication")
port = "/dev/serial0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()


def get_latitude_longitude():
    """
    Obtain and return the current latitude and longitude.
    """

    latitude = 0.0
    longitude = 0.0

    # Obtain the current location from the GPS sensor
    logger.log("Reading the GPS data") 

    while True:
        # ERROR: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfa in position 1: invalid start byte
        gps_data = ser.readline().decode("utf-8")
        if gps_data[0:6] == b'$GPGGA':
            msg = pynmea2.parse(gps_data)
            print("THE MESSAGE:\n\n")
            print(msg)
            print("")
            latitude = str(msg.latitude)
            longitude = str(msg.longitude)
        
            return latitude, longitude


import time


while True:
    latitude, longitude = get_latitude_longitude()
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")

