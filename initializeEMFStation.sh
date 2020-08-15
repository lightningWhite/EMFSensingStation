#!/bin/bash

# This will source the virtual environment for the EMF sensing station

echo 'Ensure this script is run as follows to source the current terminal:'
echo '. /home/pi/EMFSensingStation/initializeEMFStation.sh'

echo 'Sourcing the python virtual environment...'
source /home/pi/EMFSensingStation/env/bin/activate
echo 'Done.'
