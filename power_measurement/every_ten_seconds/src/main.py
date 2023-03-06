import traceback
import time

import lumen

from datetime import datetime, timezone
import requests

try:
    temp = {}
    results = []
    url = 'https://shelly-59-eu.shelly.cloud/device/status'
    data = {'channel': '0','id': 'c1a007','auth_key': 'MTZiNmMwdWlkDD12D30C6E20ED1F23258CD8F9AE728A273E5A8274CB7D9F0DBDB0394AFA0D3FD51C838BF19EB6AF'}
    r = requests.post(url, data)
    response= r.json()
    power = response["data"]["device_status"]["meters"][0]["power"]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    t = time.time()

    temp["power"] = power
    temp["datetime"] = str(now)
    temp["epoch"] = int(t)
    results.append(temp)
    for i in range(0,5):
        temp = {}
        time.sleep(10)

        r = requests.post(url, data)
        response = r.json()
        power = response["data"]["device_status"]["meters"][0]["power"]
        
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        t = time.time()
        temp["power"] = power
        temp["datetime"] = str(now)
        temp["epoch"] = int(t)
        results.append(temp)

    lumen.save({"results":results})
except Exception as e:
    lumen.save_exception(traceback.format_exc())