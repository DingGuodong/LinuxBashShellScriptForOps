## monitoring nginx

- use '[stub_status](http://nginx.org/en/docs/http/ngx_http_stub_status_module.html#stub_status)'

- use '[vts](https://github.com/vozlt/nginx-module-vts)' virtual host traffic status module

## pycharm IDE plugin for nginx

Plugin Name: `Nginx Configuration`

Features:

- Highlighting for nginx configuration files in IDE
- Comment with Line Comment action
- Structure view

[github](https://github.com/meanmail-dev/nginx-intellij-plugin)

## nginx docs

You should look at the following URL's in order to grasp a solid understanding of Nginx configuration files in order to
fully unleash the power of Nginx.

- https://www.nginx.com/resources/wiki/start/
- https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
- https://wiki.debian.org/Nginx/DirectoryStructure

## nginx acl

- 使用 allow 和 deny 指令（directives）
- 使用 .htaccess 文件

## Nginx 配置规范

> 推荐使用Git管理配置

### 文件结构 | 目录结构

1. nginx
   文件结构，建议遵循Linux发行版本文件结构布局，至少参照 [Filesystem Hierarchy Standard (FHS)](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)

### 命名规范

1. ssl 证书 命名采用域名fqdn的方式命名，如`ssl/example.com.pem`

### 其他杂项规范

- 通常来说，尽量不要直接修改`nginx.conf`， 使用 `include` 指令配置

- 修改以“最小化原则”方式进行，采用“靠近配置”，如`location > server > http`，优先选择在`location`和`server`配置，而不是配置在`http`段。

- 应该有适当的注释

- 每个业务使用独立的配置文件，公共部分或者相同部分的配置可以引用(`include`)配置文件，使用业务名或者域名命名文件或目录

- 至少要做到每一个虚拟主机都要有自己独立的日志配置，包括访问日志和错误日志

- 关于include等指令后的路径问题，建议使用绝对路径代替相对路径，除非清楚相对路径的位置

- 在`nginx -s reload`前，建议使用 `nginx -t -c nginx.conf` 进行语法检查