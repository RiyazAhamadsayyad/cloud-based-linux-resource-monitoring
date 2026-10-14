import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("logs/metrics.csv")

plt.figure(figsize=(10, 5))
plt.plot(data["cpu"])
plt.title("CPU Usage")
plt.xlabel("Samples")
plt.ylabel("CPU Usage (%)")
plt.grid()
plt.savefig("graphs/cpu_usage.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(data["memory"])
plt.title("Memory Usage")
plt.xlabel("Samples")
plt.ylabel("Memory Usage (%)")
plt.grid()
plt.savefig("graphs/memory_usage.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(data["disk"])
plt.title("Disk Usage")
plt.xlabel("Samples")
plt.ylabel("Disk Usage (%)")
plt.grid()
plt.savefig("graphs/disk_usage.png")
plt.close()

print("Graphs created successfully.")
