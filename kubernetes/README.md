#### kubernetes资源全面展示！包含K8S整体资源总览、微服务资源明细、Pod资源明细及K8S网络带宽，优化重要指标展示。



### kube-state-metrics部署说明：
```
# kube-state-metrics部署在ops-monit命名空间
kubectl create namespace ops-monit
# 选择适合K8S版本的kube-state-metrics,本仓库的kube-state-metrics镜像已经存放在阿里云. 
# 1.24以下版本的K8S安装kube-state-metrics_v2.3.0的都没问题,版本较新的K8S可以安装新版的kube-state-metrics,参考[官方](https://github.com/kubernetes/kube-state-metrics)说明.
cd kube-state-metrics
kubectl apply -f .
```
### 适合本看板的Prometheus K8S JOB配置参考
```

```
## Kubernetes for Prometheus Dashboard 使用与prometheus相关配置说明，请参考：
[https://grafana.com/grafana/dashboards/13105](https://grafana.com/grafana/dashboards/13105)

### 截图
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

### 关注公众号【**云原生DevOps**】加入运维群交流，获取更多...
![](https://github.com/starsliao/Prometheus/blob/master/qr.jpg)
### 博客：[StarsL.cn](https://starsl.cn/)

### 问题请到github上提交issue。
### GitHub：[https://github.com/starsliao/Prometheus](https://github.com/starsliao/Prometheus)
