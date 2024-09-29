#!/bin/bash

if [ $(id -u) != "0" ]; then
  echo "请使用root用户执行。"
  exit 1
fi
##部署node-exporter

if ss -nlptu|grep ":9100"
then
  echo -e "\n\n9100端口存在，请检查是否已经部署node-exporter！\n\n"
  exit 1
else
  Install_PATH=/opt/monit
  # Download_PATH='https://dingdingpushpic.oss-cn-shenzhen.aliyuncs.com/cassops/install/node_exporter-1.7.0.linux-amd64.tar.gz'
  Download_PATH='https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz'
  Filename=`echo ${Download_PATH}|awk -F / '{print $NF}'|sed 's/.tar.gz//g'`
  rm -rf ${Install_PATH}/node_exporter/
  mkdir -p ${Install_PATH}/textfile
  cd ${Install_PATH}
  wget ${Download_PATH}
  tar -zxvf ${Filename}.tar.gz
  mv ${Filename} node_exporter
  chmod +x ${Install_PATH}/node_exporter/node_exporter
  rm -rvf ${Filename}.tar.gz
  cat >/etc/systemd/system/node_exporter.service <<-EOF
[Unit]
Description=Prometheus Node Exporter
After=network.target
[Service]
Type=simple
ExecStart=${Install_PATH}/node_exporter/node_exporter \\
    --no-collector.arp \\
    --no-collector.nfs \\
    --no-collector.wifi \\
    --no-collector.ipvs \\
    --no-collector.mdadm \\
    --no-collector.zfs \\
    --no-collector.infiniband \\
    --log.level=error \\
    --web.listen-address=0.0.0.0:9100 \\
    --collector.textfile.directory=${Install_PATH}/textfile
SyslogIdentifier=node_exporter
Restart=always
[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl restart node_exporter
  systemctl enable node_exporter
  systemctl status node_exporter
  echo -e "\n\n"
  ps -ef|grep node_exporter|grep -v grep
  echo -e "\n"
  netstat -naptu|grep ":9100"
fi
