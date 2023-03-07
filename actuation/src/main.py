import traceback
import requests

import lumen

from datetime import datetime

def turn_plug_on():
    URL = "https://shelly-59-eu.shelly.cloud/device/relay/control"
    turn_on_data = {
        'channel': '0',
        'turn': 'on',
        'id': 'c1a007',
        'auth_key': 'MTZiNmMwdWlkDD12D30C6E20ED1F23258CD8F9AE728A273E5A8274CB7D9F0DBDB0394AFA0D3FD51C838BF19EB6AF'
    }
    r= requests.post(url=URL, data= turn_on_data)

def turn_plug_off():
    URL = "https://shelly-59-eu.shelly.cloud/device/relay/control"
    turn_off_data = {
    'channel': '0',
    'turn': 'off',
    'id': 'c1a007',
    'auth_key': 'MTZiNmMwdWlkDD12D30C6E20ED1F23258CD8F9AE728A273E5A8274CB7D9F0DBDB0394AFA0D3FD51C838BF19EB6AF'
    }
    r = requests.post(url=URL, data= turn_off_data)

def poll_scheduler():
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}
    data = '{"access_key": "e0efb392-55c0-4645-9c7c-385d1585b6ba", "limit": 1}'
    response = requests.post('https://sdls.lumen.live/documents/external/filter', headers=headers, data=data)
    schedule = response.json()[0]["execution-results"]["prices"]
    return(schedule)

try:
    temperature_override = 0
    if temperature_override == "too_hot": # we want to switch smart plug on as firdge is almost too warm
        turn_plug_on()
    if temperature_override == "too_cold": # we want to switch smart plug off as fridge almost too cold
        turn_plug_off()
    
    if temperature_override != "too_hot" and temperature_override != "too_cold": # we want to actuate as planned
        actuation = 1
        schedule = poll_scheduler() # getting the most recent schedule published

        now = datetime.now() # getting current datetime
        today = now.strftime("%d") # getting current day number
        month = now.strftime("%m") # getting current month
        year = now.strftime("%Y") # getting current year
        hour = now.strftime("%H") # current hour of the day
        minute = now.strftime("%M") # current minute of the hour

        minute = str(int(minute) - int(minute) % 15) # the start of the current scheduler output in minutes
        if len(minute) == 1: # if the minute is not zero padded then zero pad it
            minute = "0" + minute

        date_string = year + "-" + month + "-" + today + "T" + hour + ":" + minute + ":00" + "Z" # the date string for the start of the current scheduler output

        for time_period in schedule: # for each time step in the schedule
            if time_period["time"] == date_string: #then this is the scheduler item relating to this instant in time
                #actuation = time_period["actuation"]
                if actuation == 1:
                    turn_plug_on()
                elif actuation == 0:
                    turn_plug_off
                elif actuation != 1 and actuation != 0:
                    lumen.save_exception("Unexpected actuation signal found")



except:
    lumen.save_exception(traceback.format_exc())