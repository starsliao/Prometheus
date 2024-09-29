#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
yum install python3-devel
pip3 install psutil prometheus_client pyyaml
*/1 * * * * /usr/bin/python3 /opt/monit/linux_proc.py
"""
import sys,os,socket,psutil,yaml,datetime,urllib
from collections import Counter
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, "linux_proc.yaml")

if len(sys.argv) == 2:
    print(f'pid:{sys.argv[1]}')
    ps = psutil.Process(int(sys.argv[1]))
    iexe = ps.cmdline()[0]
    iparam = ps.cmdline()[-1]
    icwd = ps.cwd()
    psdict = {'iexe': iexe,'iparam': iparam, 'icwd': icwd}
    if not os.path.exists(yaml_path):
        try:
            res = urllib.request.urlopen('http://100.100.100.200/latest/meta-data/instance-id',timeout=1)
            iid = res.read().decode('utf-8')
        except:
            iid = f"{socket.gethostname()}_{[(s.connect(('114.114.114.114', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]}"
        cfg = {'instance': iid, 'apps': [psdict]}
    else:
        with open(yaml_path, 'r') as fy:
            cfg = yaml.load(fy, Loader=yaml.FullLoader)
            cfg['apps'].append(psdict)

    with open(yaml_path, 'w+') as fw:
        yaml.dump(cfg, fw)
    sys.exit()

with open(yaml_path, 'r') as fy:
    cfg = yaml.load(fy, Loader=yaml.FullLoader)

if datetime.datetime.now().timestamp() - os.path.getmtime(yaml_path) > 86400:
    try:
        res = urllib.request.urlopen('http://100.100.100.200/latest/meta-data/instance-id',timeout=1)
        iid = res.read().decode('utf-8')
    except:
        iid = f"{socket.gethostname()}_{[(s.connect(('114.114.114.114', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]}"
    cfg['instance'] = iid
    with open(yaml_path, 'w') as fw:
        yaml.dump(cfg, fw)
        print('update:' + yaml_path)
print(cfg)

REGISTRY = CollectorRegistry(auto_describe=False)
linux_proc_error = Gauge(f'linux_proc_error', f"LINUX_进程异常指标", ["instance", "A00_iid", "iexe", "iparam", "icwd"],registry=REGISTRY)
linux_proc_info_list = ["instance", "A00_iid", "iexe", "iparam", "icwd", "pid", "name", "status", "is_running", "exe", "cmdline", "parent", "username", "port"]
linux_proc_info = Gauge("linux_proc_info", "LINUX_进程信息指标", linux_proc_info_list,registry=REGISTRY)
metric_list = ["io_read_count","io_write_count","io_read_bytes","io_write_bytes","cpu_user","cpu_system","cpu_children_user","cpu_children_system","cpu_iowait","memory_rss","memory_vms","memory_shared","memory_swap","memory_text","memory_data","num_open_files","num_fds_limit","num_fds","cpu_num","num_threads","num_children","cpu_percent","memory_percent","durn"]

metric_dict = {}
for li in metric_list:
    metric_dict[li] = {}

instance = cfg['instance']
A00_iid = cfg['instance']
inum = 0
cpu_count = psutil.cpu_count()
for app in cfg['apps']:
    iexe = app['iexe']
    iparam = app['iparam']
    icwd = app['icwd']
    proc_app = [i for i in psutil.process_iter() if icwd == i.cwd() and iparam in i.cmdline() and iexe in i.cmdline()]
    if len(proc_app) >= 1:
        inum = inum + 1
        if len(proc_app) > 1:
            pids = [i for i in proc_app if i.ppid() == 1]
            if len(pids) >= 1:
                appinfo = pids[0]
            else:
                app_pid = Counter([i.ppid() for i in proc_app]).most_common(1)[0][0]
                appinfo = psutil.Process(app_pid)
                print(iexe,iparam,'ppid:',app_pid)
                if appinfo in proc_app:
                    pass
                else:
                    # 进程有多个，父进程不在列表中，取列表中的第一个监控
                    appinfo = proc_app[0]
                    #linux_proc_error.labels(instance, A00_iid, iexe, iparam, icwd).set(len(proc_app))
                    #continue
        else:
            appinfo = proc_app[0]
        pid = appinfo.pid
        name = appinfo.name()
        status = appinfo.status()
        is_running = appinfo.is_running()
        exe = appinfo.exe()
        cmdline = ' '.join(appinfo.cmdline())
        parent = f'{appinfo.parent().pid}/{appinfo.parent().name()}'
        durn = datetime.datetime.now().timestamp() - appinfo.create_time()
        username = appinfo.username()
        connections = appinfo.connections('all')
        port = '/'.join(sorted([f'{x.laddr.port}' for x in connections if x.status == 'LISTEN'],key=int))
        linux_proc_info.labels(instance, A00_iid, iexe, iparam, icwd, pid, name, status, is_running, exe, cmdline, parent, username, port).set(1)

        io_counters = appinfo.io_counters()
        metric_dict["io_read_count"][pid] = io_counters.read_count
        metric_dict["io_write_count"][pid] = io_counters.write_count
        metric_dict["io_read_bytes"][pid] = io_counters.read_bytes
        metric_dict["io_write_bytes"][pid] = io_counters.write_bytes

        cpu_times = appinfo.cpu_times()
        metric_dict["cpu_user"][pid] = cpu_times.user
        metric_dict["cpu_system"][pid] = cpu_times.system
        metric_dict["cpu_children_user"][pid] = cpu_times.children_user
        metric_dict["cpu_children_system"][pid] = cpu_times.children_system
        metric_dict["cpu_iowait"][pid] = cpu_times.iowait

        memory_info = appinfo.memory_full_info()
        metric_dict["memory_rss"][pid] = memory_info.rss
        metric_dict["memory_vms"][pid] = memory_info.vms
        metric_dict["memory_shared"][pid] = memory_info.shared
        metric_dict["memory_swap"][pid] = memory_info.swap
        metric_dict["memory_text"][pid] = memory_info.text
        metric_dict["memory_data"][pid] = memory_info.data

        metric_dict["num_open_files"][pid] = len(appinfo.open_files())
        metric_dict["num_fds_limit"][pid] = appinfo.rlimit(psutil.RLIMIT_NOFILE)[0]
        metric_dict["num_fds"][pid] = appinfo.num_fds()
        metric_dict["cpu_num"][pid] = appinfo.cpu_num()
        metric_dict["num_threads"][pid] = appinfo.num_threads()
        metric_dict["num_children"][pid] = len(appinfo.children())
        metric_dict["cpu_percent"][pid] = appinfo.cpu_percent(interval=1)
        #metric_dict["cpu_total_percent"][pid] = round(metric_dict["cpu_percent"][pid] / (cpu_count * 100),2) * 100
        metric_dict["memory_percent"][pid] = appinfo.memory_percent()
        metric_dict["durn"][pid] = datetime.datetime.now().timestamp() - appinfo.create_time()

        connections_sum = Counter([con.status for con in connections])
        for k,v in connections_sum.items():
            if f'conn_{k.lower()}' not in metric_dict:
                metric_dict[f'conn_{k.lower()}'] = {pid:v}
            else:
                metric_dict[f'conn_{k.lower()}'][pid] = v
    else:
        linux_proc_error.labels(instance, A00_iid, iexe, iparam, icwd).set(len(proc_app))
#print(inum, metric_dict)
if inum != 0:
    for mk,mv in metric_dict.items():
        linux_proc_metric = Gauge(f'linux_proc_{mk}', f"LINUX_进程指标：{mk}", ["instance", "A00_iid", "pid"],registry=REGISTRY)
        for ik,iv in mv.items():
            linux_proc_metric.labels(instance, A00_iid, ik).set(iv)

push_to_gateway('172.23.0.83:9091', job='push_linux_proc', grouping_key={'instance': instance}, registry=REGISTRY)
