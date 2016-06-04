import os
import datetime
import socket

try:
    import IPy
except ImportError:
    command_to_execute = "pip install IPy"
    os.system(command_to_execute)

from IPy import IP

i = datetime.datetime.now()
print i.strftime('%Y/%m/%d %H:%M:%S')

hostname = socket.getfqdn(socket.gethostname())
print hostname

ip = socket.gethostbyname(hostname)
print ip

print IP(ip).version()

print IP(ip).reverseName()
