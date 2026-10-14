import psutil
import time
from datetime import datetime

CPU_HIGH = 80
CPU_LOW = 30
RAM_HIGH = 80

print("Auto-Scaler Started")
print("Press Ctrl+C to stop")

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(
        f"{timestamp} | "
        f"CPU: {cpu:.1f}% | "
        f"RAM: {memory:.1f}%"
    )

    if cpu > CPU_HIGH or memory > RAM_HIGH:
        print("HIGH RESOURCE USAGE")
        print("SCALE UP TRIGGERED")

    elif cpu < CPU_LOW:
        print("LOW RESOURCE USAGE")
        print("SCALE DOWN TRIGGERED")

    else:
        print("RESOURCE USAGE NORMAL")

    print("-" * 50)

    time.sleep(3)
