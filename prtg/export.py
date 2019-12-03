import urllib
import sys
from datetime import datetime
from monthdelta import monthdelta

server = "http://10.0.0.32:8080"
user = "prtgadmin"
pwd = "prtgadmin"
sensors = [2035, 2028, 2026, 2037, 2039, 2036, 2027]
months = sys.argv[1:]

def df(date):
    return date.strftime("%Y-%m-%d-%H-%M-%S")

def url(sensor, start, end):
    return "{}/api/historicdata.csv?id={}&avg=0&sdate={}&edate={}&usecaption=1&username={}&password={}".format(server, sensor, df(start), df(end), user, pwd)

def export_month(month):
    for sensor in sensors:
        start = datetime.strptime(month, '%Y-%m')
        end = start + monthdelta(1)
        name = "{}-{}".format(sensor, start.strftime("%Y-%m"))
        print("exporting {}".format(name))
        urllib.urlretrieve(url(sensor, start, end), "data/{}".format(name))

for month in months:
    export_month(month)
