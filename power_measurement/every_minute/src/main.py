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
    t = time.time()

    r = requests.post(url, data)
    response= r.json()
    power = response["data"]["device_status"]["meters"][0]["power"]
    date_time_string = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    epoch = int(t*1000)

    lumen.save({"power":power,
                "epoch": epoch})
    
except Exception as e:
    lumen.save_exception(traceback.format_exc())