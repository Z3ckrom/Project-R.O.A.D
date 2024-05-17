#!/usr/bin/env python
import serial
import mysql.connector
from datetime import datetime
import os

ser = serial.Serial('/dev/ttyACM0', 9600)

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='kenneth',
    password='061499kJ',
    database='ROV_DATA'
)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROV_DATA (
        Test_Num INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE DEFAULT CURRENT_TIMESTAMP,
        Voltage DOUBLE, pH DOUBLE, Temp DOUBLE, AirQuality DOUBLE
    )
''')

conn.commit()

def script_execution():
    while True:
        arduino_data = ser.readline().decode().strip()
        print(f'Arduino Readings: {arduino_data}')

        # Extract numerical value from the received data (modify as needed)
        values = list(map(float, arduino_data.split(',')))

        # Insert the value and timestamp into the database
        cursor.execute('INSERT INTO ROV_DATA (Voltage, pH, Temp, AirQuality) VALUES (%s, %s, %s, %s)', tuple(values))
        conn.commit()

        # Create a backup folder with the current timestamp
        file_name = datetime.now().strftime('%Y-%m-%d')
        folder_path = f'/home/kenneth/shared/DATA_BACKUP/'  # Update the path

        # Ensure the folder exists, create if not
        os.makedirs(folder_path, exist_ok=True)

        # Create a new text file in the backup folder
        file_path = f'{folder_path}/{file_name}.txt'

        # Write data to the text file as a backup
        with open(file_path, 'a') as file:
            file.write(arduino_data + '\n')

# Start script execution
script_execution()

