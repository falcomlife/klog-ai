import json
from common import util
from common.args import Runtime

DATA_TRAIN_START = Runtime().ENV['data.train.start']
DATA_TRAIN_END = Runtime().ENV['data.train.end']

DATA_FORECAST_START = Runtime().ENV['data.forecast.start']
DATA_FORECAST_END = Runtime().ENV['data.forecast.end']
SAMPLE_PERIOD = Runtime().ENV['data.sample.period']
SAMPLE_STEP = Runtime().ENV['data.sample.step']
NODE_CPU_USED_PERCENTAGE_RANGE = Runtime().ENV['data.prometheus.address'] + Runtime().ENV[
    'data.node_cpu_used_percentage_range']


class DataManger():

    def __init__(self, start=DATA_FORECAST_START, end=DATA_FORECAST_END, period=SAMPLE_PERIOD, step=SAMPLE_STEP):
        self.start = start
        self.end = end
        self.period = period
        self.jsonlist = []
        self.step = step
        self.http = util.Http()

    def get_data_once(self, url, **param):
        self.http.set(url, **param)
        res = self.http.get()
        return res

    def get_all(self):
        # end = calendar.timegm(time.gmtime())
        for i in range(self.start, self.end, self.period):
            result = self.get_data_once(NODE_CPU_USED_PERCENTAGE_RANGE,
                                        **{'start': str(i), 'end': str(i + self.period), 'step': str(SAMPLE_STEP)})
            jsonobject_once = json.loads(result.content)
            self.jsonlist.append(jsonobject_once)
