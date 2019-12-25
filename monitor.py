#!/usr/bin/python3

import time
import schedule
import _thread
import os
from influxdb import InfluxDBClient

import giom
import hladiny

db = InfluxDBClient(os.getenv("GIOMON_DB_ADDRESS", "localhost"),
                    os.getenv("GIOMON_DB_PORT", "8086"), 'root', 'root', 'giomon')
db.query('CREATE DATABASE giomon WITH SHARD DURATION 30d NAME myrp')


def store_measurement(func):
    db.write_points(func())


def measure(source):
    _thread.start_new_thread(lambda: store_measurement(source), ())


schedule.every(10).seconds.do(lambda: measure(giom.measure))
schedule.every(1).minutes.do(lambda: measure(hladiny.measure))

print(f"monitor started")
while 1:
    schedule.run_pending()
    time.sleep(1)
