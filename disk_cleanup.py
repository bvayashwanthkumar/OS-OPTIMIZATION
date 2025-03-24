import os
import shutil
import tempfile
import ctypes

def delete_temp_files(temp_dir):
    """Attempt to delete files and folders in the specified temp directory."""
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)  # Delete file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)  # Delete folder
            except Exception as e:
                print(f"Skipping: {file_path} ({e})")
        print(f"✅ Cleaned: {temp_dir}")
    else:
        print(f"⚠️ Directory not found: {temp_dir}")

def clean_temp_files():
    """Cleans all temporary directories on Windows."""
    temp_dirs = [
        tempfile.gettempdir(),  # User temp folder
        os.path.expandvars(r"%SystemRoot%\Temp"),  # C:\Windows\Temp
        os.path.expandvars(r"%LOCALAPPDATA%\Temp")  # User local temp
    ]

    for temp_dir in temp_dirs:
        delete_temp_files(temp_dir)

if __name__ == "__main__":
    # Check if the script has admin rights
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("\n⚠️ Please run this script as Administrator to clean all temp files.\n")
    clean_temp_files()
    print("\n✅ Temporary files cleanup completed.")
