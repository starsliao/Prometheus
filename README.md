![](https://grafana.com/api/dashboards/8919/images/5601/image)
# Prometheus
Grafana Dashboards for Prometheus Node Exporter  
###  Grafana v5.4.2 + node_exporter 0.17 测试使用正常。
使用 Node Exporter v0.17，以实用为主，精简优化重要指标进行展示。  
包含：CPU 内存 磁盘 IO 网络 流量 温度等监控指标。  
##### Snapshot
[https://snapshot.raintank.io/dashboard/snapshot/SuYBliDVNMa1dt5FiXmwkfUCYyeBojWn](https://snapshot.raintank.io/dashboard/snapshot/SuYBliDVNMa1dt5FiXmwkfUCYyeBojWn)
#### 注意事项：
##### 需要安装饼图的插件：
```
grafana-cli plugins install grafana-piechart-panel
```
##### 请根据实际情况设置好变量后使用。
```
#env自定义的各主机环境。
$env：label_values(node_exporter_build_info,env)

#name自定义的主机名称。（跟$env关联）
$name：label_values(node_exporter_build_info{env='$env'},name)
	
#node取值node_exporter的instance，IP+端口格式。（跟$name关联查询），该看板大部分查询关联了这个变量。
#如果您无法获取$name,可修改成：label_values(node_exporter_build_info,instance)
$node：label_values(node_exporter_build_info{name='$name'},instance)

#maxmount根据$node来查询当前主机的最大分区挂载点。
$maxmount：query_result(topk(1,sort_desc (max(node_filesystem_size_bytes{instance=~'$node',fstype=~"ext4|xfs"}) by (mountpoint))))		
```
##### 关注公众号获取更多...
![](https://grafana.com/api/dashboards/8919/images/5985/image)

### 【update】：
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

![](https://grafana.com/api/dashboards/8919/images/5601/image)
