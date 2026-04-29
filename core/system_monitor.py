import psutil
import platform
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=None)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage(path='/'):
    try:
        return psutil.disk_usage(path).percent
    except:
        return 0.0


def get_top_processes(n=5):
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:n]

def get_network_usage():
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv
    }

def get_system_summary():
    return {
        "cpu": get_cpu_usage(),
        "ram": get_ram_usage(),
        "disk": get_disk_usage(),
        "network": get_network_usage(),
        "os": platform.system(),
        "version": platform.version(),
        "node": platform.node(),
        "boot_time": time.ctime(psutil.boot_time())
    }
