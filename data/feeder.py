# feeder.py
import json
import random
import time
import os
from datetime import datetime

output_dir = "/opt/spark/data/iot_stream"
os.makedirs(output_dir, exist_ok=True)

device_ids = ["sensor-1", "sensor-2", "sensor-3"]
while True:
    payload = {
        "device": random.choice(device_ids),
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(20 + random.random()*10, 2),
        "humidity": round(30 + random.random()*50, 2)
    }
    fname = datetime.utcnow().strftime("%Y%m%d%H%M%S%f") + ".json"
    with open(os.path.join(output_dir, fname), "w") as f:
        json.dump(payload, f)
    time.sleep(0.5)
