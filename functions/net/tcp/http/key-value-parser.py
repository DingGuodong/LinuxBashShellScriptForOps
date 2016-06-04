import ConfigParser
import StringIO
import os

# Read configurations
conf = StringIO.StringIO()
conf.write("[configuration]\n")
conf.write(open("key-value-config-example.conf").read())
conf.seek(0, os.SEEK_SET)
cp = ConfigParser.RawConfigParser()
cp.readfp(conf)

name = cp.get("configuration", "name")
myLove = cp.get("configuration", "mylove")
print name, "'s love is", myLove
