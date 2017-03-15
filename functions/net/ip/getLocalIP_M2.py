import os
import sys
import datetime
import socket

try:
    from IPy import IP
except ImportError:
    try:
        command_to_execute = "pip install IPy || easy_install IPy"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install IPy, Aborted!"
        sys.exit(1)
    except Exception as e:
        print "Uncaught exception, %s" % e.message
        sys.exit(1)
    from IPy import IP

i = datetime.datetime.now()
print i.strftime('%Y/%m/%d %H:%M:%S')

hostname = socket.getfqdn(socket.gethostname())
print hostname

# TODO(Guodong Ding) Get A Wrong IP Address When There Are More Than One NIC Adapter Or IP Address!!!
ip = socket.gethostbyname(hostname)
print ip

print IP(ip).version()

print IP(ip).reverseName()
