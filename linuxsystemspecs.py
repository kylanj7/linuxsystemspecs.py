import platform
import psutil
import time
import multiprocessing
import os
from datetime import datetime
import re
import subprocess

def get_system_info():
    system_info = "System Information:\n"

    # Get basic system information
    system = platform.system()
    release = platform.release()
    version = platform.version()

    system_info += f"Operating System: {system}\n"
    system_info += f"OS Release: {release}\n"
    system_info += f"OS Version: {version}\n"

    # Get detailed computer system information
    try:
        with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
            manufacturer = f.read().strip()
        with open('/sys/class/dmi/id/product_name', 'r') as f:
            model = f.read().strip()
        with open('/sys/class/dmi/id/product_serial', 'r') as f:
            serial = f.read().strip()
    except:
        manufacturer = "Unknown"
        model = "Unknown"
        serial = "Unknown"

    system_info += f"Manufacturer: {manufacturer}\n"
    system_info += f"Model: {model}\n"
    system_info += f"Serial Number: {serial}\n"

    return system_info

def get_cpu_info():
    cpu_info = "CPU Information:\n"
    
    # Get CPU details
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if 'model name' in line:
                cpu_info += f"Processor: {line.split(':')[1].strip()}\n"
                break
    
    # Get core information
    cpu_info += f"Physical cores: {psutil.cpu_count(logical=False)}\n"
    cpu_info += f"Total cores: {psutil.cpu_count(logical=True)}\n"
    
    # Get frequency information
    cpu_freq = psutil.cpu_freq()
    cpu_info += f"Max Frequency: {cpu_freq.max:.2f} MHz\n"
    cpu_info += f"Min Frequency: {cpu_freq.min:.2f} MHz\n"
    cpu_info += f"Current Frequency: {cpu_freq.current:.2f} MHz\n"
    
    return cpu_info

def get_memory_info():
    memory_info = "Memory Information:\n"

    # Total physical memory
    total_memory = psutil.virtual_memory().total / (1024**3)
    memory_info += f"Total Physical Memory: {total_memory:.2f} GB\n\n"

    # Attempt to get detailed memory information
    try:
        result = subprocess.run(['sudo', 'dmidecode', '--type', 'memory'], capture_output=True, text=True)
        if result.returncode == 0:
            memory_info += result.stdout
        else:
            memory_info += "Detailed memory information not available (requires sudo privileges)\n"
    except Exception as e:
        memory_info += f"Error retrieving detailed memory information: {str(e)}\n"

    return memory_info

def get_gpu_info():
    gpu_info = "GPU Information:\n"
    try:
        result = subprocess.run(['lspci', '-v', '-nn'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'VGA' in line or '3D' in line:
                gpu_info += line + '\n'
    except Exception as e:
        gpu_info += f"Error retrieving GPU information: {str(e)}\n"
    return gpu_info

def get_detailed_io_info():
    io_info = "Detailed I/O Information:\n"

    # USB Controllers
    io_info += "USB Controllers and Ports:\n"
    try:
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        io_info += result.stdout
    except Exception as e:
        io_info += f"Error retrieving USB information: {str(e)}\n"

    # Network Adapters
    io_info += "\nNetwork Adapters:\n"
    try:
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
        io_info += result.stdout
    except Exception as e:
        io_info += f"Error retrieving network adapter information: {str(e)}\n"

    # Audio Devices
    io_info += "\nAudio Devices:\n"
    try:
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
        io_info += result.stdout
    except Exception as e:
        io_info += f"Error retrieving audio device information: {str(e)}\n"

    # Hard Drives
    io_info += "\nHard Drives:\n"
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            io_info += f"Device: {partition.device}\n"
            io_info += f"  Mountpoint: {partition.mountpoint}\n"
            io_info += f"  File System: {partition.fstype}\n"
            io_info += f"  Total Size: {usage.total / (1024**3):.2f} GB\n"
            io_info += f"  Used: {usage.used / (1024**3):.2f} GB\n"
            io_info += f"  Free: {usage.free / (1024**3):.2f} GB\n\n"
        except PermissionError:
            io_info += f"Device: {partition.device} (Access Denied)\n\n"

    return io_info

def get_battery_health():
    battery_info = "Battery Health Information:\n"
    try:
        result = subprocess.run(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], capture_output=True, text=True)
        battery_info += result.stdout
    except Exception as e:
        battery_info += f"Error retrieving battery information: {str(e)}\n"
    return battery_info

def main():
    print("\nGathering laptop information...")
    
    info = "Laptop Testing Script Results\n"
    info += "==============================\n\n"
    info += get_system_info() + "\n"
    info += get_cpu_info() + "\n"
    info += get_memory_info() + "\n"
    info += get_gpu_info() + "\n"
    info += get_detailed_io_info() + "\n"
    info += get_battery_health() + "\n"
    
    # Get the path to the user's Documents folder
    documents_path = os.path.expanduser("~/Documents")
    
    # Create a filename with the current date and time
    filename = f"laptop_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Full path to the output file
    file_path = os.path.join(documents_path, filename)
    
    # Write the information to the file
    with open(file_path, "w") as f:
        f.write(info)
    
    print(f"Information gathered and saved to: {file_path}")
    print("Here's a summary of the information:")
    print(info)

if __name__ == "__main__":
    main()
