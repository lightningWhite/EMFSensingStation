import datetime
import emf
import gps
import logger as logging
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time

# How often the sensor readings should be logged
LOG_INTERVAL = 4#15 # seconds

# How often readings should be taken to form the average that will be logged
ACCUMULATION_INTERVAL = 2 # seconds

# Create a new file named by the current date and time
time_name = datetime.datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
data_file = "/home/pi/EMFSensingStation" + "/" +  "data" + "/" + time_name + ".csv"

logging.initialize_logger(f"/home/pi/EMFSensingStation/logs/{time_name}.log")

logging.log("The EMF sensing station has been started")
logging.log(f"Readings will be accumulated every {ACCUMULATION_INTERVAL} seconds")
logging.log(f"The data will be written every {LOG_INTERVAL} seconds")
logging.log(f"The data file is located here: {data_file}")

try:
    if not os.path.exists(os.path.dirname(data_file)):
        try:
            os.makedirs(os.path.dirname(data_file))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
    with open(data_file, "w") as file:
        # Write the labels row
        file.write("Record Number, " \
                   "Time, " \
                   "Latitude, " \
                   "Longitude, " \
                   "Avg. RF Watts (W), " \
                   "Avg. RF Watts Frequency (MHz), " \
                   "Peak RF Watts (W), " \
                   "Frequency of RF Watts Peak (MHz), "\
                   "Peak RF Watts Frequency (MHz), " \
                   "Watts of RF Watts Frequency Peak (W), " \
                   "Avg. RF Density (W m^(-2)), " \
                   "Avg. RF Density Frequency (MHz), " \
                   "Peak RF Density (W m^(-2)), " \
                   "Frequency of RF Density Peak (MHz), "\
                   "Peak RF Density Frequency (MHz), " \
                   "Density of RF Density Frequency Peak (W m^(-2)), " \
                   "Avg. Total Density (W m^(-2)), " \
                   "Max Total Density (W m^(-2)), " \
                   "Avg. EF (V/m), " \
                   "Max EF (V/m), " \
                   "Avg. EMF (mG), " \
                   "Max EMF (mG)\n")
        
    record_number = 1
    
    ###############################################################################
    # The main program loop
    ###############################################################################
    while True:
        start_time = time.time()
    
        store_rf_watts = []
        store_rf_watts_frequencies = []
        store_rf_density = []
        store_rf_density_frequencies = []
        store_rf_total_density = []
        store_ef_volts_per_meter = []
        store_emf_milligauss = []
        rf_watts = 0.0
        rf_watts_mhz_frequency = 0.0
        rf_density = 0.0
        rf_density_frequency = 0.0
        rf_total_density = 0.0
        ef_volts_per_meter = 0.0
        emf_milligauss = 0.0
    
        logging.log("Accumulating the sensor readings")
        while time.time() - start_time <= LOG_INTERVAL:
            bad_values = False

            try:
                rf_watts, rf_watts_mhz_frequency, rf_density, rf_density_frequency, rf_total_density, ef_volts_per_meter, emf_milligauss = emf.get_emf()
            except Exception as e:
                logging.log(str(e.args))
                logging.log("Not accumulating the EMF sensor values because getting the values raised an exception")
                bad_values = True

            if not bad_values: 
                store_rf_watts.append(rf_watts) 
                store_rf_watts_frequencies.append(rf_watts_mhz_frequency)
                store_rf_density.append(rf_density)
                store_rf_density_frequencies.append(rf_density_frequency)
                store_rf_total_density.append(rf_total_density)
                store_ef_volts_per_meter.append(ef_volts_per_meter)
                store_emf_milligauss.append(emf_milligauss)
    
            time.sleep(ACCUMULATION_INTERVAL)
    
        # If any of the EMF lists are empty, they all are. Set the EMF sensor values to -1.
        if len(store_rf_watts) == 0:
            logging.log("Setting the EMF values to -1 because no values were obtained from the sensor over the log period")
            store_rf_watts.append(-1) 
            store_rf_watts_frequencies.append(-1)
            store_rf_density.append(-1)
            store_rf_density_frequencies.append(-1)
            store_rf_total_density.append(-1)
            store_ef_volts_per_meter.append(-1)
            store_emf_milligauss.append(-1)

        logging.log("Calculating the max, peak, and averages of the EMF data")
    
        # Obtain the max RF watts value and its associated frequency
        rf_watts_peak = max(store_rf_watts)
        frequency_of_rf_watts_peak = round(store_rf_watts_frequencies[store_rf_watts.index(max(store_rf_watts))], 1)
    
        # Obtain the max RF watts frequency and its associated power (watts)
        rf_watts_frequency_peak = max(store_rf_watts_frequencies)
        watts_of_rf_watts_frequency_peak = store_rf_watts[store_rf_watts_frequencies.index(max(store_rf_watts_frequencies))]
    
        # Obtain the average RF power and the average frequency
        rf_watts_avg = statistics.mean(store_rf_watts)
        rf_watts_frequency_avg = round(statistics.mean(store_rf_watts_frequencies), 1)
    
    
        # Obtain the max RF density value and its associated frequency
        rf_density_peak = max(store_rf_density)
        frequency_of_rf_density_peak = round(store_rf_density_frequencies[store_rf_density.index(max(store_rf_density))], 1)
    
        # Obtain the max RF density frequency and its associated density (W m^-2)
        rf_density_frequency_peak = max(store_rf_density_frequencies)
        density_of_rf_density_frequency_peak = store_rf_density[store_rf_density_frequencies.index(max(store_rf_density_frequencies))]
    
        # Obtain the average RF power density and the average frequency
        rf_density_avg = statistics.mean(store_rf_density)
        rf_density_frequency_avg = round(statistics.mean(store_rf_density_frequencies), 1)
    
    
        # Obtain the average and max RF total density value
        rf_total_density_avg = statistics.mean(store_rf_total_density)
        rf_total_density_max = max(store_rf_total_density)
    
    
        # Obtain the average and max EF values
        ef_volts_per_meter_avg = round(statistics.mean(store_ef_volts_per_meter), 1)
        ef_volts_per_meter_max = round(max(store_ef_volts_per_meter), 1)
    
    
        # Obtain the average and max EMF values
        emf_milligauss_avg = round(statistics.mean(store_emf_milligauss), 1)
        emf_milligauss_max = round(max(store_emf_milligauss), 1)
 
        # Obtain the latitude and longitude from the GPS sensor
        latitude, longitude = gps.get_latitude_longitude()

        # This will pull from the Real Time Clock so it can be accurate
        # when there isn't an internet connection. See the readme for
        # instructions on how to configure the Real Time Clock correctly.
        current_time = datetime.datetime.now()
        
        logging.log("Printing the values obtained and calculated")
    
        print(f"Record Number:                                 {record_number}")
        print(f"Time:                                          {current_time}")
        
        # GPS Coordinates
        print(f"Latitude:                                      {latitude}")
        print(f"Longitude:                                     {longitude}")

        # RF Watts
        print(f"Avg. RF Watts (W):                             {rf_watts_avg:.16f}")
        print(f"Avg. RF Watts Frequency (MHz):                 {rf_watts_frequency_avg}")
        print(f"Peak RF Watts (W):                             {rf_watts_peak:.16f}")
        print(f"Frequency of RF Watts Peak (MHz):              {frequency_of_rf_watts_peak}")
        print(f"Peak RF Watts Frequency (MHz):                 {rf_watts_frequency_peak}")
        print(f"Watts of RF Watts Frequency Peak (W):          {watts_of_rf_watts_frequency_peak:.16f}")
    
        # RF Density
        print(f"Avg. RF Density (W m^-2):                      {rf_density_avg:.16f}")
        print(f"Avg. RF Density Frequency (MHz):               {rf_density_frequency_avg}")
        print(f"Peak RF Density (W m^-2):                      {rf_density_peak:.16f}")
        print(f"Frequency of RF Density Peak (MHz):            {frequency_of_rf_density_peak}")
        print(f"Peak RF Density Frequency (MHz):               {rf_density_frequency_peak}")
        print(f"Density of RF Density Frequency Peak (W m^-2): {density_of_rf_density_frequency_peak:.16f}")
    
        # RF Total Density 
        print(f"Avg. RF Total Density (W m^-2):                {rf_total_density_avg:.16f}")
        print(f"Max  RF Total Density (W m^-2):                {rf_total_density_max:.16f}")
    
        # EF
        print(f"Avg. EF (V/m):                                 {ef_volts_per_meter_avg}")
        print(f"Max  EF (V/m):                                 {ef_volts_per_meter_max}")
    
        # EMF
        print(f"Avg. EMF (mG):                                 {emf_milligauss_avg}")
        print(f"Max  EMF (mG):                                 {emf_milligauss_max}")
    
        print("##########################################################################")
        
        logging.log(f"Writing the data to {data_file}")
    
        # Log the data by appending the values to the data .csv file
        with open(data_file, "a") as file:
            file.write(f"{record_number}, {current_time}, " \
                       f"{latitude}, {longitude}, " \
                       f"{rf_watts_avg:.16f}, {rf_watts_frequency_avg}, " \
                       f"{rf_watts_peak:.16f}, {frequency_of_rf_watts_peak}, " \
                       f"{rf_watts_frequency_peak}, {watts_of_rf_watts_frequency_peak:.16f}, " \
                       f"{rf_density_avg:.16f}, {rf_density_frequency_avg}, " \
                       f"{rf_density_peak:.16f}, {frequency_of_rf_density_peak}, " \
                       f"{rf_density_frequency_peak}, {density_of_rf_density_frequency_peak:.16f}, " \
                       f"{rf_total_density_avg:.16f}, {rf_total_density_max:.16f}, " \
                       f"{ef_volts_per_meter_avg}, {ef_volts_per_meter_max}, " \
                       f"{emf_milligauss_avg}, {emf_milligauss_max}\n")
    
        # Check if an external USB storage device is connected
        check_external_drive = subprocess.Popen(
            'df -h | grep /dev/sda1',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)    
        stdout, stderr = check_external_drive.communicate()
    
        # Copy the newly written file to the external USB drive if one is connected
        if len(stdout) > 0:
            file_name = time_name + '.csv'
            backup_name = time_name + '.csv' + '.bak'
            logging.log(f"Backing up the data to /mnt/usb1/{file_name}")
            
            # Change the name of the last backup so we don't overwrite it until
            # the latest backup is obtained
            rename_old_backup_data = subprocess.Popen(
                f"mv /mnt/usb1/{file_name} /mnt/usb1/{backup_name}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            stdout, stderr = rename_old_backup_data.communicate()
    
            # Get the latest data file to the external drive
            backup_data = subprocess.Popen(
                f"cp {data_file} /mnt/usb1/{file_name}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            stdout, stderr = backup_data.communicate()
        else:
            print("WARNING: The data is not being backed up. Ensure an external storage device is connected.")
            logging.log("WARNING: The data is not being backed up. Ensure an external storage device is connected.")
    
        # Clear the recorded values so they can be updated over the next LOG_INTERVAL
        store_rf_watts.clear()
        store_rf_watts_frequencies.clear() 
        store_rf_density.clear()
        store_rf_density_frequencies.clear()
        store_rf_total_density.clear()
        store_ef_volts_per_meter.clear()
        store_emf_milligauss.clear()
    
        record_number = record_number + 1

except Exception as e:
    logging.log("An unhandled exception occurred causing a crash: " + str(e.args))

