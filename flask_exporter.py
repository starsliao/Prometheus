#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-
import prometheus_client
from prometheus_client import Gauge,Info
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import psutil
app = Flask(__name__)
REGISTRY = CollectorRegistry(auto_describe=False)
mem = Gauge('memory', 'memory info',['memtype'],registry=REGISTRY)
i = Info('my_build_version', 'Description of info',registry=REGISTRY)

@app.route("/metrics")
def hahah():
    mem.labels(memtype='total').set(psutil.virtual_memory().total)
    mem.labels(memtype='available').set(psutil.virtual_memory().available)
    mem.labels(memtype='used').set(psutil.virtual_memory().used)
    i.info({'version': '1.2.3', 'buildhost': 'foo@bar'})
    return Response(prometheus_client.generate_latest(REGISTRY),mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
