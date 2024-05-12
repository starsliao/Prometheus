## K8S Dashboard CN 20240513 StarsL.cn 下载地址:
[https://grafana.com/grafana/dashboards/13105](https://grafana.com/grafana/dashboards/13105)
### Grafana看板ID: 13105
#### kubernetes资源全面展示！包含K8S整体资源总览、微服务资源明细、Pod资源明细及K8S网络带宽，优化重要指标展示。
### 更新说明
##### v20240513
1. 更新了看板的所有Panel支持最新样式,优化展示性能,已兼容Grafana10.X版本.
2. 增加了K8S总体的状态条展示节点与微服务资源的统计.
3. 增加了PVC的使用情况,各命名空间的CPU,内存使用曲线图.
4. 优化了Pod与微服务资源明细表格的展示字段与视觉效果.
5. 优化了Pod与微服务CPU与内存使用量的曲线图中可以直接展示出该资源的Limit值红线.
6. 修复了Pod重启导致短时间内展示的Pod资源数据不准确的BUG.
7. 调整了多个图表,曲线图的展示效果与描述,优化部分指标数据更加精准。
8. 增加了各个版本的kube-state-metrics国内镜像.
9. 增加了Prometheus on K8S的JOB配置说明.
##### v20211010
1. 基于K8S总可用资源的维度，修改了各类资源总可用量的指标，指标更加精准。
2. 支持`kube-state-metrics_v2.x`并兼容`kube-state-metrics_v1.9.x`。
3. 所有表格使用了新的表格样式，并且对各字段颜色做了处理。
4. 根据节点、微服务、Pod维度调整了图表展示效果。
5. 提供了`kube-state-metrics_v1.9.8`和`kube-state-metrics_v2.2.1`的部署文件和国内源。参考[【这里】](https://github.com/starsliao/Prometheus/tree/master/kubernetes)
##### v20201209
1. 使用`Filter by name`来优化了表格展示的字段。
2. 增加了关于节点名称标签在不同指标中不一致的说明。  
##### v20201208
1. 调整了资源总览页的展示效果。
2. 增加了更多命名空间维度的统计信息。
3. 总览页的节点明细表格更新为grafana7的样式，增加了各节点资源的使用比例并标记颜色。
4. 微服务和pod的表格数据与曲线图分开2个卡片展示，表格中可以直接查看微服务及对应Pod的明细。
5. 曲线图使用独立的卡片展示，浏览所有微服务表格时，不会出现服务过多引起卡顿的情况，建议制定微服务后在查看曲线图。
6. 优化了部分图表的描述。
### 截图
---
#### 整体资源总览
![](https://grafana.com/api/dashboards/13105/images/16207/image)
![](https://grafana.com/api/dashboards/13105/images/16208/image)
#### Pod资源明细
![](https://grafana.com/api/dashboards/13105/images/16209/image)
#### 微服务资源明细
![](https://grafana.com/api/dashboards/13105/images/16210/image)

### 赞赏与关注公众号【**云原生DevOps**】加入交流群（请备注：K8S），获取更多...

**如果看不到图片请点击该链接：[https://starsl.cn/static/img/thanks.png](https://starsl.cn/static/img/thanks.png)**
![](https://starsl.cn/static/img/thanks.png)

---

### kube-state-metrics部署说明：
- kube-state-metrics部署在ops-monit命名空间
- 选择适合K8S版本的kube-state-metrics,本仓库的kube-state-metrics镜像已经存放在阿里云. 
- 1.24以下版本的K8S安装kube-state-metrics_v2.3.0的都没问题,版本较新的K8S可以安装新版的kube-state-metrics,参考[官方](https://github.com/kubernetes/kube-state-metrics)说明.
```
kubectl create namespace ops-monit
cd kube-state-metrics_vXXX
kubectl apply -f .
```
### 适合本看板的Prometheus K8S JOB配置参考
- 说明: 本配置适合于Prometheus部署在K8S内的场景.
- **注意: 关于节点名称的标签，因为`cadvisor`是使用`instance`，而`kube-state-metrics`是使用`node`；这样会导致节点信息表格中，没有统一的字段来连接各个查询，所以`cadvisor`的job下需要复制一个`node`标签。**
```
    metric_relabel_configs:
    - source_labels: [instance]
      separator: ;
      regex: (.+)
      target_label: node
      replacement: $1
      action: replace
```
- 以下是本看板必须的3个JOB配置
- `k8s-kubelet`和`k8s-cadvisor` JOB都是各节点的kubelet自带的指标.
- `kube-state-metrics` JOB是安装的`kube-state-metrics`的指标.
```
  - job_name: 'k8s-kubelet'
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    kubernetes_sd_configs:
    - role: node
    relabel_configs:
    - target_label: __address__
      replacement: kubernetes.default.svc:443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics

  - job_name: 'k8s-cadvisor'
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    kubernetes_sd_configs:
    - role: node
    relabel_configs:
    - target_label: __address__
      replacement: kubernetes.default.svc:443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
    metric_relabel_configs:
    - source_labels: [instance]
      separator: ;
      regex: (.+)
      target_label: node
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
```
