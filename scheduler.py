import psutil
import os

def get_processes():
    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(processes, key=lambda p: p['cpu_percent'])  # Sort by CPU usage

def optimize_processes():
    processes = get_processes()
    print("Optimizing process scheduling...\n")
    for process in processes[:5]:  # Optimize only the top 5 least CPU-consuming processes
        try:
            os.system(f"renice +10 -p {process['pid']}")  # Lower priority (Linux/Mac)
            print(f"Optimized process: {process['name']} (PID: {process['pid']})")
        except Exception as e:
            print(f"Failed to optimize {process['name']}: {e}")

if __name__ == "__main__":
    optimize_processes()
    print("\nProcess optimization completed.")
