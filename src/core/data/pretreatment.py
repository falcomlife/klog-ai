import datetime
import json
import time
import numpy as np

from common.args import Runtime
from data.premetheus import DataManger

cpu_data_range = {}


def cpu_data_pretreatment():
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    dt = str(y) + '-' + str(m) + '-' + str(d) + ' 00:00:00'
    start = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    end = int(time.time())

    # start = int(Runtime().ENV['data.forecast.start'])
    # end = int(Runtime().ENV['data.forecast.end'])

    # start = int(Runtime().ENV['data.train.start'])
    # end = int(Runtime().ENV['data.train.end'])

    datamanage = DataManger(start, end, int(Runtime().ENV['data.sample.period']))
    datamanage.get_all()
    for item in datamanage.jsonlist:
        if item['status'] == 'success':
            if item['data']['result']:
                for res in item['data']['result']:
                    instance = res['metric']['instance']
                    values = res['values']
                    if instance not in cpu_data_range:
                        cpu_data_range[instance] = {'index': [], 'columns': ['precent'], 'data': []}
                    for time_data in values:
                        cpu_data_range[instance]['index'].append(time_data[0])
                        s = []
                        s.append(time_data[1])
                        cpu_data_range[instance]['data'].append(s)
    return cpu_data_range
    # with open("/home/sorawingwind/workhome/program/python/AnomalyDetection/src/source/10-16-record.json", "w") as f:
    #     json.dump(cpu_data_range, f)


def read_train_data():
    with open("/home/sorawingwind/workhome/program/python/AnomalyDetection/src/source/05-06-record.json",
              'r') as load_f:
        cpu_data_range = json.load(load_f)
        return cpu_data_range


def read_forecast_data():
    with open("/home/sorawingwind/workhome/program/python/AnomalyDetection/src/source/05-07-record.json",
              'r') as load_f:
        cpu_data_range = json.load(load_f)
        return cpu_data_range


def data_reader(cpu_data_range):
    ins = {}
    for instance, data in cpu_data_range.items():
        timestamps = data["index"]
        datas = data["data"]
        items = []
        for index, time in enumerate(timestamps):
            item = [time, datas[index][0]]
            items.append(item)
        ins[instance] = np.array(items)
    return ins