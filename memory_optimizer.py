import os

def clean_memory():
    print("Cleaning memory...")
    os.system("sync; echo 3 > /proc/sys/vm/drop_caches")  # Linux-specific

clean_memory()
