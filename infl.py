#!/usr/bin/env python

import datetime
import psutil
import time
from influxdb import InfluxDBClient

import secrets as sec

# influx configuration - edit these
ifuser = sec.gr_user
ifpass = sec.gr_pw
ifdb   = "home"
ifhost = sec.gr_host
ifport = sec.gr_port
measurement_name = "system"

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
while True:

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
    
    print(body)


    time.sleep(5)

    ifclient.write_points(body)
