## InfluxDB notes

install InfluxDB on Debian/Ubuntu Linux

```shell
sudo apt install influxdb influxdb-client -y
influx -execute 'CREATE DATABASE "prometheus"'
influx -precision rfc3339
```

default port: 8086