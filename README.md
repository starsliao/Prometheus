### Blackbox Exporter 0.14 for Prometheus 监控展示看板
>目前在使用的TCP，ICMP，HTTPS服务状态监控 Prometheus Blackbox Exporter，在一个看板里面展示，做了展示效果的优化，支持多服务同时展示，需要使用的可以参考下，记得根据自己的实际情况修改下变量。
### 记得安装饼图插件
![](https://raw.githubusercontent.com/starsliao/Prometheus/master/blackbox-exporter.png)

##  Grafana v5.4.2 +  node_exporter 0.16 、node_exporter 0.17 测试使用正常。
使用 Node Exporter v0.17，以实用为主，精简优化重要指标进行展示。  
包含：CPU 内存 磁盘 IO 网络 流量 温度等监控指标。  
##### 截图
![](https://raw.githubusercontent.com/starsliao/Prometheus/master/screenshot.jpg)
##### 关注公众号【**全栈运维开发 Python & Vue**】获取更多...
![](https://raw.githubusercontent.com/starsliao/Prometheus/master/qr.png)
#### 注意事项：
##### 需要安装饼图的插件：
```
grafana-cli plugins install grafana-piechart-panel
# 请确保安装后能正常添加饼图。
```
---
#### 请根据实际情况在grafana该面板的设置中配置好变量后使用：

- **必须：`$node`取值node_exporter的`instance`，IP+端口格式。该看板大部分查询关联了这个变量，请确保该变量有效**：
  - 注意：在Prometheus中使用`count(node_exporter_build_info) by(instance,version)`查询各node的instance格式和版本。
```
跟$name关联查询：
label_values(node_exporter_build_info{name='$name'},instance)

如果您无法获取$name,可修改成：
label_values(node_exporter_build_info,instance)
```
---
- 重要：`$maxmount`用于根据`$node`来查询当前主机的最大分区挂载点。
```
query_result(topk(1,sort_desc (max(node_filesystem_size_bytes{instance=~'$node',fstype=~"ext4|xfs"}) by (mountpoint))))
```
---
- 可选：`$env`自定义的各主机环境：
```
label_values(node_exporter_build_info,env)
```
---
- 可选：`$name`自定义的主机名称。（跟`$env`关联）：
```
label_values(node_exporter_build_info{env='$env'},name)
```
### 【update】：
##### 2019/1/9
1. 修复了一个展示内存使用量不准确的bug。
2. 增加了更新node_exporter和仪表板的外链。
3. Grafana v5.4.2 + node_exporter 0.16 、node_exporter 0.17 测试使用正常。
##### 11/16
1. 增加了变量的说明。
2. 优化了新安装看板后的展示速度。 
##### 11/15  
1. 增加各环境对服务器分组。
2. 增加饼图，磁盘总空间。
3. 增加当前打开文件描述符。
4. 增加部分监控指标的描述。
5. 优化部分指标的显示结果。
##### 11/13  
1. 增加磁盘每秒的I/O操作耗费时间占比图形。  
