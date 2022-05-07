
# 推荐使用【ConsulManager】来管理主机监控与站点监控
## [【ConsulManager介绍】](https://github.com/starsliao/ConsulManager)
- ### [应用场景1：如何优雅的基于Consul自动同步ECS主机监控](https://github.com/starsliao/ConsulManager/blob/main/docs/ECS%E4%B8%BB%E6%9C%BA%E7%9B%91%E6%8E%A7.md)
- ### [应用场景2：如何优雅的使用Consul管理Blackbox站点监控](https://github.com/starsliao/ConsulManager/blob/main/docs/blackbox%E7%AB%99%E7%82%B9%E7%9B%91%E6%8E%A7.md)

---

### Blackbox Exporter Dashboard
- 支持Grafana 8，基于blackbox_exporter 0.19.0设计
- 采用图表+曲线图方式展示TCP，ICMP，HTTPS的服务状态，各阶段请求延时，HTTPS证书信息等
- 优化展示效果，支持监控目标的分组、分类级联展示，多服务同时对比展示。

导入ID：9965
详细URL：https://grafana.com/grafana/dashboards/9965

![](https://raw.githubusercontent.com/starsliao/ConsulManager/main/screenshot/blackbox1.PNG)
![](https://raw.githubusercontent.com/starsliao/ConsulManager/main/screenshot/blackbox2.PNG)
![](https://raw.githubusercontent.com/starsliao/ConsulManager/main/screenshot/blackbox3.PNG)
![](https://raw.githubusercontent.com/starsliao/ConsulManager/main/screenshot/blackbox4.PNG)
![](https://raw.githubusercontent.com/starsliao/ConsulManager/main/vue-consul/public/blackbox.png)
