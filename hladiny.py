from urllib import request
import json
from datetime import datetime

flatten = lambda l: [item for sublist in l for item in sublist]


def url(id):
    return f'https://www.hladiny.cz/cz/outputs/json/st_{id}.json'


def measurement(name, value, date):
    return {"measurement": name,
            "time": date.isoformat(),
            "fields": {
                "value": value
            }}


def fetch(id):
    res = request.urlopen(url(id))
    data = json.loads(res.read())
    name = data['label1']
    date = datetime.fromtimestamp(int(data['ch_last_data']['0']))
    value = float(data['ch_value']['0'])
    history = data['ch_history']['0']
    measurements = [measurement(name, value, date)]
    for timestamp in history.keys():
        measurements.append(measurement(name, float(history[timestamp]), datetime.fromtimestamp(int(timestamp))))

    return measurements


sensors = [42525, 42522, 42514]


def measure():
    print(f'taking hladiny measurement @ {datetime.utcnow()}')
    return flatten(list(map(fetch, sensors)))
