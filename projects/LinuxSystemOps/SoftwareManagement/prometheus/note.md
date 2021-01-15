# notes for prometheus

## what is Prometheus

什么是 Prometheus

Monitoring system and time series database

## Prometheus 主要功能

Prometheus由Go语言编写而成，采用Pull方式获取监控信息，并提供了多维度的数据模型和灵活的查询接口。

Prometheus不仅可以通过静态文件配置监控对象，还支持自动发现机制，能够通过Kubernetes、Consul、DNS等多种方式动态获取监控对象。

## Prometheus 不能做什么

- Prometheus 的数据是基于时序的 float64 的值，如果你的数据值有更多类型，无法满足。
- Prometheus 不适合做审计计费，因为它的数据是按一定时间采集的，会造成数据丢失。 Prometheus关注的更多是系统的运行瞬时状态以及趋势，即使有少量数据没有采集也能容忍， 但是审计计费需要记录每个请求，并且数据长期存储，这个
  Prometheus 无法满足，可能需要采用专门的审计系统。
- Prometheus 不适合存储文本（日志），因此不能作为日志存储解决方案

## Prometheus vs Zabbix

- Zabbix 使用的是C和PHP, Prometheus使用Golang, 依赖较少，整体而言Prometheus运行速度更快一点。
- Zabbix 属于传统主机监控，主要用于物理主机，交换机，网络等监控，Prometheus 不仅适用主机监控，还适用于 Cloud, SaaS, Openstack，Container 监控。
- Zabbix 在传统主机监控方面，有更多可选的插件。
- Zabbix 可以在Web GUI中配置很多事情，但是Prometheus需要手动修改文件配置。
- Prometheus 数据查询语句表现力更强大，内置更强大的统计函数。

> 建议：在彻底掌控之前，使用Zabbix用于传统IT架构，而是用Prometheus用于云原生、微服务等新型IT架构。

## float64

- Double-precision floating-point format
- store value in 64 bits length in memory

## deploy prometheus on Linux OS amd64 Arch

```shell
PROMETHEUS_VERSION=2.24.0
PROMETHEUS_BASEDIR=/opt/prometheus
wget -c https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
tar -zxvf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz -C /opt
ln -s /opt/prometheus-${PROMETHEUS_VERSION}.linux-amd64 ${PROMETHEUS_BASEDIR}
cd ${PROMETHEUS_BASEDIR}
```

or

```shell
sudo apt install prometheus -y
```

## start prometheus

```shell
PROMETHEUS_BASEDIR=/opt/prometheus
cd ${PROMETHEUS_BASEDIR}
./prometheus --version
./prometheus --config.file=prometheus.yml
```

> 在生产环境中，我们可以将 Prometheus 添加到sysv或systemd里，或者使用supervisord作为服务自启动。

## default prometheus port

9090

## metric type

- counter，计数器，只能累加metric，只增不减（除非系统发生重置），记录某些事件发生的次数，用于了解该事件产生速率的变化 一般在定义Counter类型指标的名称时推荐使用_total作为后缀
  http_requests_total
- gauge，仪表盘，任意加减变化的metric，侧重于反应系统的当前状态 node_memory_MemFree（主机当前空闲的内容大小）、node_memory_MemAvailable（可用内存大小）
- histogram，柱状图、直方图，用于统计和分析样本的分布情况，可以对观察结果采样，分组及统计。
- summary，摘要，用于统计和分析样本的分布情况
- untyped

> 需要特别注意的是，假设采样数据 metric 叫做 x, 如果 x 是 histogram 或 summary 类型必需满足以下条件：
> - 采样数据的总和应表示为 x_sum。
> - 采样数据的总量应表示为 x_count。
> - summary 类型的采样数据的 quantile 应表示为 x{quantile="y"}。
> - histogram 类型的采样分区统计数据将表示为 x_bucket{le="y"}。
> - histogram 类型的采样必须包含 x_bucket{le="+Inf"}, 它的值等于 x_count 的值。
> - summary 和 historam 中 quantile 和 le 必需按从小到大顺序排列。

## exporter

- node_exporter
- wmi_exporter
- mysqld_exporter
- redis_exporter
- blackbox_exporter

### start node exporter

```shell
./node_exporter --web.listen-address 127.0.0.1:8080
```

[configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)

## reload prometheus configuration

```shell
kill -SIGHUP <prometheus pid>
```

## good example configuration file

https://github.com/prometheus/prometheus/blob/release-2.24/config/testdata/conf.good.yml

## PromSQL

https://prometheus.io/docs/querying/basics/

聚合函数

- sum (求和)
- min (最小值)
- max (最大值)
- avg (平均值)
- stddev (标准差)
- stdvar (标准方差)
- count (计数)
- count_values (对value进行计数)
- bottomk (后n条时序)
- topk (前n条时序)
- quantile (分位数)

内置函数

- increase （平均增长率）
- rate （平均增长速率）
- irate （瞬时增长率）
- predict_linear （预测，基于线性回归）
- histogram_quantile （分位数计算）

## exporters

[exporters and integrations](https://prometheus.io/docs/instrumenting/exporters/#exporters-and-integrations)

## Pushgateway

use 'push' instead of 'pull'

## Alertmanager

## 容量计算

在一般情况下，Prometheus中存储的每一个样本大概占用1-2字节(1byte=8bits， 字节为存储存储单位，“字节”表示用于编码单个字符所需要的比特数量)大小。 如果需要对Prometheus
Server的本地磁盘空间做容量规划时，可以通过以下公式计算：

```
needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample
```

从上面公式中可以看出在保留时间(retention_time_seconds)和样本大小(bytes_per_sample)不变的情况下，如果想减少本地磁盘的容量需求， 只能通过减少每秒获取样本数(
ingested_samples_per_second)的方式。 因此有两种手段，一是减少时间序列的数量，二是增加采集样本的时间间隔。 考虑到Prometheus会对时间序列进行压缩效率，减少时间序列的数量效果更明显。

## 使用InfluxDB存储、读写数据

```yaml
# Set remote read/write use local influxdb database
remote_write:
  - url: "http://localhost:8086/api/v1/prom/write?db=prometheus"

remote_read:
  - url: "http://localhost:8086/api/v1/prom/read?db=prometheus"
```

## Grafana

```shell
GRAFANA_VERSION=7.3.6
GRAFANA_BASEDIR=/opt/grafana
wget -c https://dl.grafana.com/oss/release/grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz
tar -zxvf grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz -C /opt
ln -s /opt/grafana-${GRAFANA_VERSION} ${GRAFANA_BASEDIR}
cd ${GRAFANA_BASEDIR}

```

default port: 3000 default user: admin default password: admin

> 也可以考虑使用grafana做报警发送

## prometheus client libraries

[prometheus client libraries](https://prometheus.io/docs/instrumenting/clientlibs/)
[Prometheus Python Client](https://github.com/prometheus/client_python)

## Google/mtail

[mtail](https://github.com/google/mtail)日志处理器是由Google的SRE人员使用Go语言编写的，专门用于从应用程序日志中提取要导出到时间序列数据库中的指标，从无法导出自己内部状态的应用程序中解析日志数据。

## Black exporter

[Blackbox exporter](https://github.com/prometheus/blackbox_exporter)允许通过HTTP、HTTPS、DNS、TCP和ICMP来探测端点，执行检查并将生成的指标返回给Prometheus。

> Tips: 条件允许的情况下，还是云原生（Cloud Native）支持最好，直接暴露metric给Prometheus。
> 因为过多的exporter会占用较多的服务端口号和主机性能。

default port: 9115

## ansible-prometheus

[Ansible Role: prometheus](https://github.com/cloudalchemy/ansible-prometheus)

## 参考书

- 《Prometheus监控实战》詹姆斯·特恩布尔 机械工业出版社 2019年8月
- 《Prometheus云原生监控：运维与开发实战》 朱政科 机械工业出版社 2020年10月
- 《深入浅出Prometheus：原理、应用、源码与拓展详解》陈晓宇等 电子工业出版社 2019年4月
- 《Prometheus 监控技术与实践》 陈金窗等 机械工业出版社 2020年03月01