**v20201208版本总览表格使用grafana 7的样式，不支持grafana 6.x。建议升级到grafana 7，使用新版表格获得更好的展示效果。**  
如果使用的是grafana 6.x，请下载[v20201010版](https://grafana.com/api/dashboards/13105/revisions/3/download)并编辑json文件，把`table-old`替换成`table`，再导入到grafana即可。

### kube-state-metrics部署：
```
# kube-state-metrics部署在ops-monit命名空间
kubectl create namespace ops-monit
cd kube-state-metrics
kubectl apply -f .
```
## Kubernetes for Prometheus Dashboard 使用：
[https://grafana.com/grafana/dashboards/13105](https://grafana.com/grafana/dashboards/13105)

---
新增数据源变量`origin_prometheus`，取自于Prometheus的外部系统标签：`external_labels`，可用于支持多个Prometheus接入VictoriaMetrics或Thanos等第三方存储使用`remote_write`方式的场景。(默认取值空，指标中无该标签不影响使用)  
**`VictoriaMetrics`请使用v1.42.0及以上版本，修复了grafana表格展示的问题。**
---
### 更新说明：
**v20201208**
1. 调整了资源总览页的展示效果。
2. 增加了更多命名空间维度的统计信息。
3. 总览页的节点明细表格更新为grafana7的样式，增加了各节点资源的使用比例并标记颜色。
4. 微服务和pod的表格数据与曲线图分开2个卡片展示，表格中可以直接查看微服务及对应Pod的明细。
5. 曲线图使用独立的卡片展示，浏览所有微服务表格时，不会出现服务过多引起卡顿的情况，建议制定微服务后在查看曲线图。
6. 优化了部分图表的描述。
---
#### 整体资源总览
![](https://grafana.com/api/dashboards/13105/images/9490/image)
#### 微服务资源明细
![](https://grafana.com/api/dashboards/13105/images/9021/image)
#### Pod资源明细
![](https://grafana.com/api/dashboards/13105/images/9022/image)
#### K8S网络带宽
![](https://grafana.com/api/dashboards/13105/images/9023/image)
---
**注意：Prometheus需要能采集到`cadvisor`与`kube-state-metrics`的指标。**
- cAdvisor作为kubelet内置的一部分程序可以直接使用。
- kube-state-metrics部署可参考：[https://github.com/starsliao/Prometheus/tree/master/kubernetes](https://github.com/starsliao/Prometheus/tree/master/kubernetes)
#### Prometheus job配置参考（kube-state-metrics部署在ops-monit命名空间）：
```
  - job_name: 'k8s-cadvisor'
    metrics_path: /metrics/cadvisor
    kubernetes_sd_configs:
    - role: node
    relabel_configs:
    - source_labels: [__address__]
      regex: '(.*):10250'
      replacement: '${1}:10255'
      target_label: __address__
      action: replace
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)

    metric_relabel_configs:
    - source_labels: [instance]
      separator: ;
      regex: (.+)
      target_label: node
      replacement: $1
      action: replace

    - source_labels: [pod_name]
      separator: ;
      regex: (.+)
      target_label: pod
      replacement: $1
      action: replace
    - source_labels: [container_name]
      separator: ;
      regex: (.+)
      target_label: container
      replacement: $1
      action: replace

  - job_name: kube-state-metrics
    kubernetes_sd_configs:
    - role: endpoints
      namespaces:
        names:
        - ops-monit
    relabel_configs:
    - source_labels: [__meta_kubernetes_service_label_app_kubernetes_io_name]
      regex: kube-state-metrics
      replacement: $1
      action: keep
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: k8s_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: k8s_sname
```
---
### 关注公众号【**全栈运维开发**】加入运维群交流，获取更多...
![](https://starsl.cn/static/img/qr.png)
### 博客：[StarsL.cn](https://starsl.cn/)

### 问题请到github上提交issue。
### GitHub：[https://github.com/starsliao/Prometheus](https://github.com/starsliao/Prometheus)
