#!/usr/bin/env python

import datetime
import psutil
import time
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "<yourpassword>"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "system"

# take a timestamp for this measurement
curr_time = datetime.datetime.utcnow()

# collect some stats from psutil
disk = psutil.disk_usage('/')
mem = psutil.virtual_memory()
load = psutil.cpu_percent()

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": curr_time,
        
        "fields": {
            "load": load,
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
while True:
    time.sleep(5)
    ifclient.write_points(body)