import socket
import psutil
from datetime import datetime

def ingb(bytes_value):
    return bytes_value / (1024**3)

def get_private_ip():
    interfaces = psutil.net_if_addrs()
    for interface_name, addresses in interfaces.items():
        for address in addresses:
            if address.family == socket.AF_INET:
                if not address.address.startswith("127."):
                    return interface_name, address.address
    return "No private IP found"

def cpu():
    cpu_percent = psutil.cpu_percent(interval=1)
#    core_percent = psutil.cpu_percent(interval=1,percpu=True)
#    cpu_count = psutil.cpu_count()

    print(f"CPU Usage: {cpu_percent}%")
#    for i in range(cpu_count):
#        print(f"Core {i+1}: {core_percent[i]}%")

def ram():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print(f"RAM: {ingb(ram[3]):.1f}GB / {ingb(ram[0]):.1f}GB")
    print(f"Swap: {ingb(swap[1]):.1f}GB / {ingb(swap[0]):.1f}GB")

def disk():
    seen = set()

    for partition in psutil.disk_partitions():
        if partition.fstype in ("tmpfs", "squashfs"):
            continue

        if partition.device in seen:
            continue

        seen.add(partition.device)

        disk = psutil.disk_usage(partition.mountpoint)

        mount_text = f"({partition.mountpoint})"

        print(f"{mount_text}"
              f" {ingb(disk[1]):.1f}GB / "
              f"{ingb(disk[0]):.1f}GB ({disk[3]}%)")

def network():
    io = psutil.net_io_counters()
    upload_mb = float(io.bytes_sent) / 1048576
    download_mb = float(io.bytes_recv) / 1048576

    print(
            f"Interface: {get_private_ip()[0]}\n"
            f"IP: {get_private_ip()[1]}\n"
            f"Upload: {upload_mb:.1f}MB\n"
            f"Download: {download_mb:.1f}MB")

def uptime():
    uptime = int(datetime.now().timestamp() - psutil.boot_time())

    days, remainder = divmod(uptime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        uptime_string = f"{days}d {hours}h {minutes}m"
    else:
        uptime_string = f"{hours}h {minutes}m {seconds}s"

    print(f"Uptime: {uptime_string}")

print("\n=======     SYSTEM STATUS     =======\n")
cpu()
ram()
print("")
network()
print("")
uptime()
print("\nDisk Usage: ")
disk()
print("\n=====================================")
