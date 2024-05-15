### 使用kafka_exporter监控多kafka
> kafka_exporter项目地址：https://github.com/danielqsj/kafka_exporter

- 使用docker-compose部署多个kafka_exporter，每个exporter对接一个kafka。
- 注意：配置上每个kafka broker的地址，kafka3需要指定版本。
```
version: '3.1'
services:
  kafka-exporter-opslogs:
    image: bitnami/kafka-exporter:latest
    command:
      - '--kafka.server=10.2.19.43:9092'
      - '--kafka.server=10.2.24.62:9092'
      - '--kafka.server=10.5.98.190:9092'
      - '--kafka.version=3.2.1'
    restart: always
    ports:
      - 9310:9308

  kafka-exporter-prod:
    image: bitnami/kafka-exporter:latest
    command:
      - '--kafka.server=192.168.53.99:9092'
      - '--kafka.server=192.168.53.53:9092'
      - '--kafka.server=192.168.53.96:9092'
    restart: always
    ports:
      - 9311:9308
```
### Promethus配置job接入kafka-exporter
- 注意：每个kafka-exporter必须增加`name`标签，看板需要使用这个标签。
```
  - job_name: 'kafka-exporter'
    metrics_path: /metrics
    scrape_interval: 15s
    scrape_timeout: 10s
    static_configs:
    - targets:
      - 10.0.0.26:9310
      labels:
        name: kafka-opslogs
    - targets:
      - 10.0.0.26:9311
      labels:
        name: kafka-prod
```
### KAFKA Grafana Dashboard
##### 【中文版本】2024.05.16更新，基于Prometheus的kafka_exporter，KAFKA资源展示、问题排查、快速积压分析！
- 看板的所有Panel支持最新样式,优化展示性能,已兼容Grafana10.X版本.
- 包括KAFKA整体的资源状态，
- 生产者与消费者关系
- 消息积压的明细信息
- 生产与消费的速率
- 异常的消费与Topic展示
- 分区级别的积压与消费明细

### 赞赏与关注公众号【**云原生DevOps**】加入交流群（请备注：K8S），获取更多...

**如果看不到图片请点击该链接：[https://starsl.cn/static/img/thanks.png](https://starsl.cn/static/img/thanks.png)**
![](https://starsl.cn/static/img/thanks.png)

### 截图
- 全局信息、消费者与Topic、异常与积压分析
![](https://grafana.com/api/dashboards/21078/images/16236/image)
- 分区维度明细
![](https://grafana.com/api/dashboards/21078/images/16237/image)

### 看板下载
- Grafana看板ID：21078
- Grafana看板地址：https://grafana.com/grafana/dashboards/21078
- 项目仓库：https://github.com/starsliao/Prometheus/kafka

### Prometheus告警规则
```
- name: kafka
  rules:
  - alert: KAFKA_brokers异常
    expr: kafka_broker_info != 1
    for: 2m
    labels:
      severity: critical
    annotations:
      description: "{{ $labels.name }}当前brokers异常：{{ $labels.address }}"

  - alert: 电商生产KAFKA消息整体积压
    expr: sum(kafka_consumergroup_lag_sum{job="kafka-exporter"}) by (name,consumergroup, topic)>5000
    for: 2m
    labels:
      severity: critical
    annotations:
      description: "【环境】{{ $labels.name }}\n【消费组】{{ $labels.consumergroup }}\n【topic】{{ $labels.topic }}【积压】：{{ $value | printf \"%.2f\" }}"

  - alert: 电商生产KAFKA消息分区积压
    expr: (sum(kafka_consumergroup_lag{job="kafka-exporter"}) by (name,consumergroup, topic, partition)>1500) AND ON() (hour()+8)%24 >= 7 <= 21
    for: 3m
    labels:
      severity: critical
    annotations:
      description: "【环境】{{ $labels.name }}\n【消费组】{{ $labels.consumergroup }}\n【topic】{{$labels.topic}}【分区】{{ $labels.partition }}【积压】：{{ $value | printf \"%.2f\" }}"

  - alert: 电商生产KAFKA分区数过多
    expr: sum by(name)(kafka_topic_partitions{job="kafka-exporter",topic !~"__.*"})>1500
    for: 2m
    labels:
      severity: critical
    annotations:
      description: "{{ $labels.name }}当前分区数：{{ $value | printf \"%.2f\" }}"

  - alert: 电商生产KAFKA_brokers丢失
    expr: kafka_brokers{job="kafka-exporter"} < 3
    for: 2m
    labels:
      severity: critical
    annotations:
      description: "{{ $labels.name }}当前brokers数：{{ $value | printf \"%.2f\" }}"

  - alert: 电商生产KAFKA_TopicsReplicas
    expr: sum(kafka_topic_partition_in_sync_replica{job="kafka-exporter"}) by (name,topic) <1
    for: 2m
    labels:
      severity: critical
    annotations:
      description: "{{ $labels.name }} Kafka topic in-sync partition：{{ $value | printf \"%.2f\" }}"
```
