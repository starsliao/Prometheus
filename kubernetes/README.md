#### 【中文版本】2020.10.03更新，kubernetes资源全面展示！包含K8S整体资源总览、微服务资源明细、Pod资源明细及K8S网络带宽，优化重要指标展示。

#### kube-state-metrics部署：
```
#kube-state-metrics部署在ops-monit命名空间
kubectl create namespace ops-monit
cd kube-state-metrics
kubectl apply -f .
```

#### Kubernetes for Prometheus Dashboard 使用：
https://grafana.com/grafana/dashboards/13105
