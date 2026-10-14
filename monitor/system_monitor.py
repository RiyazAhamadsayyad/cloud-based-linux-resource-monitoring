import psutil
import time
import csv
import os
from datetime import datetime

LOG_FILE = "logs/metrics.csv"

os.makedirs("logs", exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cpu", "memory", "disk"])

print("Linux Resource Monitor Started")
print("Press Ctrl+C to stop")

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu, memory, disk])

    print(
        f"{timestamp} | "
        f"CPU: {cpu:.1f}% | "
        f"RAM: {memory:.1f}% | "
        f"Disk: {disk:.1f}%"
    )

    time.sleep(2)

