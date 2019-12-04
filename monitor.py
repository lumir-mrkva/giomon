#!/usr/bin/python3

from xml.dom import minidom
from datetime import datetime
import time
import pytz
import schedule
import _thread
import os
from urllib import request

from influxdb import InfluxDBClient

interval = 10  # seconds
giom = os.getenv("GIOMON_GIOM", "http://10.0.0.5")
db = InfluxDBClient(os.getenv("GIOMON_DB_ADDRESS", "localhost"),
                    os.getenv("GIOMON_DB_PORT", "8086"), 'root', 'root', 'giomon')
db.query('CREATE DATABASE giomon WITH SHARD DURATION 30d NAME myrp')


def measure():
    date = datetime.now()
    date = pytz.timezone("Europe/Prague").localize(date)
    # print(f'taking measurement @ {date}')
    xml = request.urlopen(f'{giom}/status.xml').read()
    status = minidom.parseString(xml)

    def value(measurement):
        return float(status.getElementsByTagName(measurement)[0].firstChild.data)

    def measurement(name, value):
        return {"measurement": name,
                "time": date.isoformat(),
                "fields": {
                    "value": value
                }}

    data = [
        measurement("Rychlost_vetru", value("windspeed")),
        measurement("Wind_direction_degr.", (360 / 16) * value("winddir")),
        measurement("Wind_GUST", value("windgust")),
        measurement("Relative_Pressure", value("pressure")),
        measurement("Sys_temp", value("systemp")),
        measurement("Teplota", value("temperature")),
        measurement("Barometric_altitude", value("baraltitude")),
        measurement("Windchill", value("windchill")),
        measurement("Relative_humidity", value("relhumidity")),
        measurement("Absolute_humidity", value("abshumidity")),
        measurement("Dew_point", value("dewpoint")),
    ]

    db.write_points(data)


def measure_async():
    _thread.start_new_thread(measure, ())


schedule.every(interval).seconds.do(measure_async)

print(f"taking measurement every {interval} seconds")
while 1:
    schedule.run_pending()
    time.sleep(1)
