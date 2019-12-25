from xml.dom import minidom
from datetime import datetime
import os
from urllib import request

giom = os.getenv("GIOMON_GIOM", "http://10.0.0.5")


def measure():
    date = datetime.utcnow()
    print(f'taking giom measurement @ {date}')
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

    return [
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
