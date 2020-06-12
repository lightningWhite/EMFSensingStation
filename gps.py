# GPS Sensor
#
# Uses the GT-U7 module to obtain GPS information.
#
# GPGGA NMEA returns the following fields
# GPGGA - the message type
# timestamp - UTC time in hours, minutes, and seconds
# latitude - in DDMM.MMMMM format. Decimal places are variable
# latitude direction
# longitude - in DDMM.MMMMM format
# longitude direction
# fix quality
# number of satellites used in the coordinate
# horizontal dilution of precision
# altitude of the antenna
# units of altitude
# height of geoid above WGS84 ellipsoid
# units used by the geoid separation
# age of the correction (if any)
# correction station id (if any)
# checksum
#
# Ensure the following connections:
# 
# GND of the GPS sensor to GND on the Pi
# VCC of the GPS sensor to 3v3 on the Pi
# RX of the GPS sensor to BCM 14 on the Pi
# TX of the GPS sensor to BCM 15 on the Pi
#
# Also ensure that serial is enabled on the Pi.

import serial
import pynmea2
import logger

# Uncomment this line when testing this module alone
# logger.initialize_logger("/home/pi/EMFSensingStation/logs/test.log")

# Set up the GPS serial port connection
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

        try:
            # Read the serial stream from the GPS sensor
            gps_data = ser.readline()
            gps_data = gps_data.decode("utf-8")

            # Obtain the lat/long from the GPGGA data string
            if gps_data[0:6] == '$GPGGA':
                # Parse the GPGGA string
                msg = pynmea2.parse(gps_data)
                
                # Obtain the latitude and longitude from the string
                latitude = str(msg.latitude)
                longitude = str(msg.longitude)

                return latitude, longitude

        except Exception as e:
            logging.log(str(e.args))
            logging.log("An exception was thrown while obtaining the GPS data. Continuing.")
            continue

# Uncomment the lines below for testing this module alone
#while True:
#    latitude, longitude = get_latitude_longitude()
#    print(f"Latitude: {latitude}")
#    print(f"Longitude: {longitude}")

