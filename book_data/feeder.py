import json
import random
import time
import os
from datetime import datetime

output_dir = "/opt/spark/data/iot_stream"
os.makedirs(output_dir, exist_ok=True)

device_ids = ["sensor-1", "sensor-2", "sensor-3"]

try:
    while True:
        now = datetime.utcnow()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")

        payload = {
            "device": random.choice(device_ids),
            "timestamp": timestamp_str,
            "temperature": round(20 + random.random() * 10, 2),
            "humidity": round(30 + random.random() * 50, 2)
        }

        fname = f"{now.strftime('%Y%m%d%H%M%S%f')}_{random.randint(0, 9999):04d}.json"
        filepath = os.path.join(output_dir, fname)

        with open(filepath, "w") as f:
            json.dump(payload, f)

        print(f"Wrote: {fname}")  # Add logging
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Feeder stopped by user.")

    # docker exec -d da-spark-master python3 /opt/spark/data/feeder.py
# docker exec -it da-spark-master spark-submit /opt/spark/data/streaming_job.py
# docker exec da-spark-master chmod -R a+rw /opt/spark/data
# Make run
