# Prometheus
Grafana Dashboards for Prometheus Node Exporter  

使用 Node Exporter v0.16，精简优化重要指标展示。  
包含：CPU 内存 磁盘 IO 网络 流量 温度等监控指标。  
##### 安装
[Grafana Dashboards](https://grafana.com/orgs/starsliao/dashboards)
##### 预览
[https://snapshot.raintank.io/dashboard/snapshot/SuYBliDVNMa1dt5FiXmwkfUCYyeBojWn](https://snapshot.raintank.io/dashboard/snapshot/SuYBliDVNMa1dt5FiXmwkfUCYyeBojWn)
##### 需要安装饼图的插件：
```
grafana-cli plugins install grafana-piechart-panel
```
### 【update】：
##### 11/15  
1. 增加各环境对服务器分组
2. 增加饼图，磁盘总空间
3. 增加当前打开文件描述符
4. 增加部分监控指标的描述
5. 优化部分指标的显示结果
##### 11/13  
1. 增加磁盘每秒的I/O操作耗费时间占比图形
