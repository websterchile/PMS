#read sensor data(temp and vibrations) from ESP32 and save to a sqlite database
import serial  
import sqlite3
import time
from datetime import datetime
# Database connection
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
