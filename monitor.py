import psutil
import time

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Disk Usage: {disk_usage.percent}%\n")

while True:
    get_system_stats()
    time.sleep(5)  # Collect data every 5 seconds
