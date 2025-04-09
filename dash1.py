import streamlit as st
import psutil
import platform
import time
import os
import shutil
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="System Dashboard", layout="wide", page_icon="💻")

# Inject custom CSS for a dark theme
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        .main, .block-container {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        h1, h2, h3, h4 {
            color: #00adb5;
        }
        .stApp {
            background-color: #1e1e1e;
        }
        .stMarkdown p {
            font-size: 20px;
            color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Title and layout
st.markdown("""
    <h1 style='text-align: center; color: #00adb5; font-size: 3em; text-shadow: 1px 1px #000;'>
        💻 Advanced System Optimization Dashboard
    </h1>
    <hr style='border: 1px solid #00adb5;' />
""", unsafe_allow_html=True)

# System Information
col1, col2 = st.columns(2)
with col1:
    st.header("🖥️ System Info")
    st.markdown(f"**OS:** {platform.system()} {platform.release()}")
    st.markdown(f"**Processor:** {platform.processor()}")
    st.markdown(f"**Machine:** {platform.machine()}")
    st.markdown(f"**Python Version:** {platform.python_version()}")
    st.markdown(f"**Boot Time:** {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.header("❤️ System Health")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    st.progress(cpu / 100, text=f"CPU Usage: {cpu}%")
    st.progress(mem / 100, text=f"Memory Usage: {mem}%")
    st.progress(disk / 100, text=f"Disk Usage: {disk}%")

st.markdown("---")

# Memory Optimizer (Linux Only)
def memory_cleanup():
    os.system('sync; echo 3 > /proc/sys/vm/drop_caches')

def show_memory_tools():
    st.header("🧠 Memory Optimization")
    if platform.system() == "Linux":
        if st.button("Run Memory Cleanup"):
            memory_cleanup()
            st.success("Memory cleanup executed.")
    else:
        st.warning("Memory cleanup is supported only on Linux.")

show_memory_tools()
st.markdown("---")

# Disk Cleanup
def disk_cleanup():
    temp_dir = os.getenv('TEMP') or '/tmp'
    try:
        for root, dirs, files in os.walk(temp_dir):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    continue
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name))
                except:
                    continue
        return True
    except Exception as e:
        return False
# Disk Cleanup
st.header("🧹 Disk Cleanup")
with st.expander("Check Disk Usage"):
    usage = psutil.disk_usage('/')
    st.write(f"Total: {usage.total / (1024 ** 3):.2f} GB")
    st.write(f"Used: {usage.used / (1024 ** 3):.2f} GB")
    st.write(f"Free: {usage.free / (1024 ** 3):.2f} GB")
    st.write(f"Percentage Used: {usage.percent}%")

if st.button("Clean Temporary Files"):
    if disk_cleanup():
        st.success("Temporary files cleaned up successfully.")
    else:
        st.error("Disk cleanup failed.")

st.markdown("---")

# Top Memory Apps (Live update)
st.header("🔍 Top Memory Consuming Apps")
if 'last_top_processes' not in st.session_state:
    st.session_state.last_top_processes = []

refresh = st.button("Refresh Top Memory Apps")

if refresh or True:
    processes = [(p.info['pid'], p.info['name'], p.info['memory_percent'])
                 for p in psutil.process_iter(['pid', 'name', 'memory_percent'])]
    processes.sort(key=lambda x: x[2], reverse=True)
    st.session_state.last_top_processes = processes[:5]

for pid, name, memory in st.session_state.last_top_processes:
    st.write(f"**{name}** (PID: {pid}) - {memory:.2f}%")

st.markdown("---")

# Kill Process
st.header("❌ Kill Process")
process_id = st.text_input("Enter Process ID to Kill", "")
if st.button("Kill Process"):
    if process_id.isdigit():
        try:
            p = psutil.Process(int(process_id))
            p.terminate()
            st.success(f"Process {process_id} terminated.")
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter a valid numeric PID.")

st.markdown("---")

# Live CPU Usage Chart (Real-time)
st.header("📈 Live CPU Usage (Real-Time)")

if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
    st.session_state.cpu_data = pd.DataFrame({'Time': [], 'CPU Usage': []})

start_stop = st.button("Start Monitoring" if not st.session_state.monitoring else "Stop Monitoring")

if start_stop:
    st.session_state.monitoring = not st.session_state.monitoring

cpu_placeholder = st.empty()

if st.session_state.monitoring:
    for _ in range(20):
        current_time = datetime.now().strftime('%H:%M:%S')
        cpu_percent = psutil.cpu_percent()
        new_row = pd.DataFrame({'Time': [current_time], 'CPU Usage': [cpu_percent]})
        st.session_state.cpu_data = pd.concat([st.session_state.cpu_data, new_row]).tail(20)

        cpu_chart_data = st.session_state.cpu_data.set_index('Time')
        cpu_placeholder.line_chart(cpu_chart_data)

        time.sleep(1)


st.markdown("---")

# Live System Health
st.header("📊 Live System Status")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
with col2:
    st.metric("Memory Usage", f"{psutil.virtual_memory().percent}%")
with col3:
    st.metric("Disk Usage", f"{psutil.disk_usage('/').percent}%")

st.markdown("---")

# Load Average
if platform.system() != "Windows":
    st.header("📊 Load Average (Unix only)")
    load1, load5, load15 = os.getloadavg()
    st.write(f"1-minute Load Average: {load1:.2f}")
    st.write(f"5-minute Load Average: {load5:.2f}")
    st.write(f"15-minute Load Average: {load15:.2f}")

# Startup Programs and Swap
st.header("🛠️ Optimization Insights")
if hasattr(psutil, 'swap_memory'):
    swap = psutil.swap_memory()
    st.write(f"Swap Total: {swap.total / (1024 ** 3):.2f} GB")
    st.write(f"Swap Used: {swap.used / (1024 ** 3):.2f} GB")
    st.write(f"Swap Usage: {swap.percent}%")


st.header("🧠 Auto Optimization Suggestions")

high_mem_threshold = 10.0
high_cpu_threshold = 50.0

# Gather processes info
high_resource_processes = []
for p in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
    try:
        if p.info['memory_percent'] > high_mem_threshold or p.info['cpu_percent'] > high_cpu_threshold:
            high_resource_processes.append(p.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

if high_resource_processes:
    st.warning("⚠️ Resource-Intensive Processes Detected:")
    df = pd.DataFrame(high_resource_processes)
    df = df.sort_values(by=["memory_percent", "cpu_percent"], ascending=False)
    st.dataframe(df[["pid", "name", "memory_percent", "cpu_percent"]].rename(columns={
        "pid": "PID", "name": "Process Name",
        "memory_percent": "Memory (%)", "cpu_percent": "CPU (%)"
    }), use_container_width=True)

    st.markdown("💡 **Suggestions:**")
    st.markdown("- Consider terminating unused applications consuming high memory or CPU.")
    st.markdown("- Investigate background processes that are not essential.")
    st.markdown("- Reboot system if usage remains high after optimizations.")
else:
    st.success("✅ System resource usage is within optimal limits.")

st.markdown("---")
st.caption("Team Members :- Vijay Kumar , Yashwanth Kumar BVA , Arpita Yadav")