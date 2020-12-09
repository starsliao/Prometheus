#### kubernetes资源全面展示！包含K8S整体资源总览、微服务资源明细、Pod资源明细及K8S网络带宽，优化重要指标展示。



### kube-state-metrics部署说明：
```
# kube-state-metrics部署在ops-monit命名空间
kubectl create namespace ops-monit
cd kube-state-metrics
kubectl apply -f .
```
## Kubernetes for Prometheus Dashboard 使用与配置说明：
[https://grafana.com/grafana/dashboards/13105](https://grafana.com/grafana/dashboards/13105)

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
