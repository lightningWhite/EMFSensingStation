#!/bin/bash

# /etc/init.d/startEMFStation.sh
### BEGIN INIT INFO
# Provides:          startEMFStation.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon EMF sensing station at boot time
# Description:       Start daemon EMF sensing station at boot time
### END INIT INFO


# This script will start the EMF sensing station in a tmux terminal and then
# detach it. This makes it so the ssh session can time out or be terminated and
# the EMF station process will remain running. Using tmux also allows the
# user to attach to the session at any time and view the real-time output of the
# program.

echo "Starting the EMF sensing station..."

# Start the EMF sensing station in a tmux terminal and then detach it
tmux new-session -d -s emf_station ". /home/pi/EMFSensingStation/initializeEMFStation.sh && python3 -u /home/pi/EMFSensingStation/emf_station.py && tmux detach"

# Wait before checking if it started successfully
sleep 2

# Naively check if the process started
if ps -a | grep python3
then
  echo "The EMF sensing station has been started."
  echo "The data location is at /home/pi/EMFSensingStation/data/"
  echo "The log output can be found in logs/" 
  echo "To view the real-time output of the process, run 'tmux attach'"
  echo "To detach and keep the process running after exiting the ssh session, type 'Ctrl+b' and then 'd' before logging out"
else
  echo "The EMF sensing station failed to start. Ensure everything is connected correctly."
fi

