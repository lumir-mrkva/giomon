from influxdb import InfluxDBClient
from datetime import datetime, timezone
import csv
import sys
import pytz

server = "10.0.0.54"
port = 8086
files = sys.argv[1:]

for file in files:
    print(f'importing {file}')
    name = ''
    data = []
    with open(file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                name = str(list(row.keys())[2]).replace (" ", "_")
                print(f'measurement {name}')
                line_count += 1
            try:
                date = datetime.strptime(row['Date Time'], '%m/%d/%Y %I:%M:%S %p')
                date = pytz.timezone("Europe/Prague").localize(date)
                data.append({"measurement": name,
                             "time": date.isoformat(),
                             "fields": {
                                 "value": float(list(row.values())[3])
                             }})
                #print(data[len(data)-1])
            except ValueError:
                pass
            line_count += 1
    if len(data) > 0:
        print(f'from {data[0]["time"]} to {data[len(data)-1]["time"]}')
        db = InfluxDBClient(server, port, 'root', 'root', 'giomon')
        db.query('CREATE DATABASE giomon WITH SHARD DURATION 30d NAME myrp')
        db.write_points(data)
    print(f'imported {len(data)} measurements')
