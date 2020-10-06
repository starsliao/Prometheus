### 基于推送方式的进程监控脚本
说明：监控进程所在主机无需启动后台服务方式监控，而是使用定时任务来推送监控指标到pushgateway。
1. 部署Pushgateway并增加到Prometheus
```
mkdir /opt/pushgateway/
wget https://github.com/prometheus/pushgateway/releases/download/v1.3.0/pushgateway-1.3.0.linux-amd64.tar.gz -O /opt/pushgateway/pushgateway-1.3.0.linux-amd64.tar.gz
cd /opt/pushgateway/
tar -zxvf pushgateway-1.3.0.linux-amd64.tar.gz

cat > /etc/systemd/system/pushgateway.service <<EOF
[Unit]
Description=pushgateway
After=syslog.target network.target
[Service]
Type=simple
RemainAfterExit=no
WorkingDirectory=/opt/pushgateway
ExecStart=/opt/pushgateway/pushgateway \\
  --web.listen-address=:9091 \\
  --web.telemetry-path=/metrics \\
  --persistence.interval=5m \\
  --persistence.file=/opt/pushgateway/pers-data
SyslogIdentifier=pushgateway
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable pushgateway
systemctl start pushgateway
```
```
vi prometheus.yml
  - job_name: 'pushgateway'
    static_configs:
    - targets: ['pushgateway:9091']
    honor_labels: true
```
2. 部署监控客户端
```
yum install python3-devel
pip3 install psutil prometheus_client pyyaml
mkdir /opt/monit
wegt 
```
