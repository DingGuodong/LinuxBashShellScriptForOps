import os
import datetime

try:
    import psutil
except ImportError:
    command_to_execute = "pip install psutil"
    os.system(command_to_execute)
import psutil

cpu = psutil.cpu_times()
print cpu
print cpu.system
print cpu.user
print cpu.idle

mem = psutil.virtual_memory()
print mem.total
print mem.free
print mem.used

swap = psutil.swap_memory()
print swap.total
print swap.free
print swap.used

disk = psutil.disk_partitions()
print disk

disk_io = psutil.disk_io_counters(perdisk=True)
print disk_io
print disk_io.get('PhysicalDrive1')
print disk_io.get('PhysicalDrive0')

user = psutil.users()
print user

boot_time = psutil.boot_time()
print datetime.datetime.fromtimestamp(boot_time).strftime("%H:%M:%S %Y/%m/%d")

net_io = psutil.net_io_counters()
print net_io.bytes_recv
print net_io.bytes_sent
print net_io[1]
print net_io[0]
print net_io
