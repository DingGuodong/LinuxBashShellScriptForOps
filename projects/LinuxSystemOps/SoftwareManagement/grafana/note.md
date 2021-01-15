## Grafana notes

install Grafana on Debian/Ubuntu Linux

```shell
# https://grafana.com/grafana/download
sudo apt-get install -y adduser libfontconfig1
wget -c https://dl.grafana.com/oss/release/grafana_7.3.6_amd64.deb
sudo dpkg -i grafana_7.3.6_amd64.deb
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable grafana-server
sudo /bin/systemctl start grafana-server
```

## import template

Official & community built dashboards:

- [Prometheus Node Exporter Full](https://grafana.com/grafana/dashboards/1860)

- [Node Exporter for Prometheus Dashboard CN v20201010](https://grafana.com/grafana/dashboards/8919)

- [Node Exporter for Prometheus Dashboard EN v20201010](https://grafana.com/grafana/dashboards/11074)
