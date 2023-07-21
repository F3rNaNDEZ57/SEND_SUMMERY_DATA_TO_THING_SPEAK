import os.path
import gspread
import json
from google.oauth2.service_account import Credentials
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from apscheduler.schedulers.background import BackgroundScheduler
import time

def send_data_to_thingspeak():
    # Your existing code here...

scheduler = BackgroundScheduler()
scheduler.add_job(send_data_to_thingspeak, 'interval', minutes=5)
scheduler.start()

# This is here to simulate application activity (which keeps the main thread alive).
try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
