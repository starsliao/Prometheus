### 🎉Node Exporter Grafana Dashboard 更新啦!

#### **Node Exporter Dashboard分为2个版本**

- **🌟TenSunS自动同步版：通过TenSunS来管理各云厂商的ECS监控**：支持在云厂商对资源增删改查后，自动同步到Prometheus（同时也支持自建主机的批量web管理与同步）。采集云厂商的ECS信息(包括到期日)与分组等信息，基于采集的数据实现了更友好、丰富的资源分组，以及云资源名称等多种云标签的搜索与展示。

- **原基于Job分组的通用版**：对于不使用TenSunS同步资源的情况，资源标签信息较少，仅可以使用通用的JOB字段来分组。

---

### 2024.05.20更新说明：
1. 更新了看板的所有Panel支持最新样式，对大量图表重新做了美化，已兼容Grafana10.X版本。
2. 总览表优化ECS健康评分加载性能，增加了更多图表的说明描述。
3. 新增了整体资源消耗信息的一些图表，用于资源成本优化参考。
4. 使用了从云厂商获取的ECS名称字段和新的分组字段，并且能展示资源到期日。
5. 优化重要指标展示，包含整体资源展示与资源明细图表：CPU 内存 磁盘 进程 网络等监控指标。

##### 注意:【最近7天P99资源使用率】图表需要在Prometheus增加记录规则(采集1小时后出数据)：

- P99：数据集按升序排列，第99分位置大的数据。（即升序排列后排在99%位置的数据）
- 该表格需要在Prometheus增加记录规则（参考看板下载页）
- 采集1小时后出数据
- 时间范围[7d:1h]表示要查看过去 7 天内每小时的数据点。

---

##### TenSunS自动同步版增加记录规则

```
groups: #新rule文件需要加这行开头，追加旧的rule文件则不需要。
- name: node_usage_record_rules
  interval: 1m
  rules:
  - record: cpu:usage:rate1m
    expr: (1 - avg(irate(node_cpu_seconds_total{mode="idle"}[3m])) by (instance,vendor,account,group,name)) * 100
  - record: mem:usage:rate1m
    expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

##### 基于Job分组的通用版增加记录规则
- Job分组的通用版的数据源变量origin_prometheus，取自于Prometheus的外部系统标签：external_labels，可用于支持多个Prometheus接入VictoriaMetrics或Thanos等第三方存储使用remote_write方式的场景。(默认取值空，指标中无该标签不影响使用)
```
groups:   #新rule文件需要加这行开头，追加旧的rule文件则不需要。
- name: node_usage_record_rules
  interval: 1m
  rules:
  - record: cpu:usage:rate1m
    expr: (1 - avg(irate(node_cpu_seconds_total{mode="idle"}[3m])) by (instance,job)) * 100
  - record: mem:usage:rate1m
    expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```
---

### TenSunS自动同步版看板请配合TenSunS使用
#### [📌点击进入【TenSunS介绍】https://github.com/starsliao/TenSunS](https://github.com/starsliao/TenSunS)
#### [🥇最佳实践 https://github.com/starsliao/TenSunS?tab=readme-ov-file#最佳实践](https://github.com/starsliao/TenSunS?tab=readme-ov-file#%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5)
- [应用场景1：如何优雅的基于Consul自动同步ECS主机监控](https://github.com/starsliao/ConsulManager/blob/main/docs/ECS%E4%B8%BB%E6%9C%BA%E7%9B%91%E6%8E%A7.md)
- [应用场景2：如何优雅的使用Consul管理Blackbox站点监控](https://github.com/starsliao/ConsulManager/blob/main/docs/blackbox%E7%AB%99%E7%82%B9%E7%9B%91%E6%8E%A7.md)
- [应用场景3：如何把云主机自动同步到JumpServer](https://github.com/starsliao/ConsulManager/blob/main/docs/%E5%A6%82%E4%BD%95%E6%8A%8A%E4%B8%BB%E6%9C%BA%E8%87%AA%E5%8A%A8%E5%90%8C%E6%AD%A5%E5%88%B0JumpServer.md)
- [应用场景4：使用1个mysqld_exporter监控所有的MySQL实例](https://github.com/starsliao/ConsulManager/blob/main/docs/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E4%BD%BF%E7%94%A8%E4%B8%80%E4%B8%AAmysqld_exporter%E7%9B%91%E6%8E%A7%E6%89%80%E6%9C%89%E7%9A%84MySQL%E5%AE%9E%E4%BE%8B.md)
- [应用场景5：使用1个redis_exporter监控所有的Redis实例](https://github.com/starsliao/ConsulManager/blob/main/docs/%E4%BD%BF%E7%94%A8%E4%B8%80%E4%B8%AAredis_exporter%E7%9B%91%E6%8E%A7%E6%89%80%E6%9C%89%E7%9A%84Redis%E5%AE%9E%E4%BE%8B.md)

---

### TenSunS部分功能描述
#### 自建与云资源监控管理(ECS/RDS/Redis)
>**基于Consul实现Prometheus监控目标的自动发现。**

- ✔**当前已支持对接阿里云、腾讯云、华为云。**

  - ⭐支持多云ECS/RDS/Redis的**资源、分组、标签**自动同步到Consul并接入到Prometheus自动发现！(并提供云资源信息查询与自定义页面)
  - ⭐支持多云ECS信息自动同步到**JumpServer**。
  - ⭐支持多云**账户余额**与云资源**到期日**设置阈值告警通知。
  - ⭐支持作为Exporter接入Prometheus：Prometheus增加ConsulManager的JOB后可抓取云厂商的部分MySQL/Redis指标。(弥补原生Exporter无法获取部分云MySQL/Redis指标的问题)
- ✔**支持自建主机/MySQL/Redis**接入WEB管理，支持增删改查、批量导入导出，自动同步到Consul并接入到Prometheus监控！
- ✔提供了按需生成Prometheus配置与ECS/MySQL/Redis告警规则的功能。
- ✔设计了多个支持同步的各字段展示的Node_Exporter、Mysqld_Exporter、Redis_Exporter Grafana看板。

截图：
![](https://grafana.com/api/dashboards/8919/images/16268/image)
![](https://grafana.com/api/dashboards/8919/images/16269/image)
![](https://grafana.com/api/dashboards/8919/images/16270/image)
![](https://grafana.com/api/dashboards/8919/images/16271/image)
![](https://grafana.com/api/dashboards/8919/images/16272/image)
![](https://grafana.com/api/dashboards/8919/images/16273/image)
![](https://grafana.com/api/dashboards/8919/images/16274/image)

### 赞赏与关注公众号【云原生DevOps】加入运维群交流，获取更多...
![](https://starsl.cn/static/img/thanks.png)
#### GitHub：[https://github.com/starsliao/TenSunS](https://github.com/starsliao/TenSunS)

### 看板下载

**我的全部Grafana看板**
- https://grafana.com/orgs/starsliao/dashboards

**TenSunS自动同步版**
- Grafana ID: 8919
- https://grafana.com/grafana/dashboards/8919

**通用Job分组版**
- Grafana ID: 16098
- https://grafana.com/grafana/dashboards/16098
