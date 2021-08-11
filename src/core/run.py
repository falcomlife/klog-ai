# dev
#import matplotlib
#matplotlib.use('TkAgg')
import resource
import json
import pandas as pd
from common.args import Runtime
from data.dataset import Dataset
from data.pretreatment import read_train_data, data_reader, cpu_data_pretreatment,read_forecast_data
from model.forecast import forecast
from model.train import train, valid, see

CORE_RUN_STEP = Runtime().ENV['core.run.step']
CORE_TRAIN_TYPE = Runtime().ENV['core.train.type']
DATASET_TIME_STEP = Runtime().ENV['dataset.time.step']
# soft,hard = resource.getrlimit(resource.RLIMIT_AS)
# resource.setrlimit(resource.RLIMIT_AS,(10*1024^6,hard))

if __name__ == '__main__':
    print("start", CORE_RUN_STEP, "step")
    if CORE_RUN_STEP == "data":
        cpu_data_pretreatment()
    elif CORE_RUN_STEP == 'train' or CORE_RUN_STEP == 'valid' or CORE_RUN_STEP == 'see':
        for instance, data in read_train_data().items():
            train_json = pd.read_json(json.dumps(data), orient='split')
            training_mean = train_json.mean()
            training_std = train_json.std()
            df_training_value = (train_json - training_mean) / training_std
            # 实例化数据集
            train_dataset = Dataset(df_training_value.values, DATASET_TIME_STEP)
            if CORE_RUN_STEP == 'train':
                train(instance, train_dataset, None,CORE_TRAIN_TYPE)
            elif CORE_RUN_STEP == 'valid':
                valid(instance, train_dataset)
            elif CORE_RUN_STEP == 'see':
                see(instance, train_dataset)
    elif CORE_RUN_STEP == 'forecast':
        cpu_data_range = cpu_data_pretreatment()
        idatas = data_reader(cpu_data_range)
        for instance, data in cpu_data_range.items():
            forecast_json = pd.read_json(json.dumps(data), orient='split')
            forecast_mean = forecast_json.mean()
            forecast_std = forecast_json.std()
            df_forecast_value = (forecast_json - forecast_mean) / forecast_std
            # 实例化数据集
            forecast_dataset = Dataset(df_forecast_value.values, DATASET_TIME_STEP)
            forecast(instance, forecast_dataset, idatas[instance], forecast_json)
    print("job has finished")
