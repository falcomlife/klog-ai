# 探测异常数据
import json
import math
import os
import time
import uuid
from datetime import timedelta

import numpy as np

from common.args import Runtime
from common.db import DB
from entity.Result import Result
from model.auto_encoder import AutoEncoder
import paddle
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from common.config import config as cfg
from dateutil.tz import tzoffset
from sqlalchemy import String, DateTime, Text

ξ = 0.5772156649  # 欧拉常数


def forecast(instance, a_forecast_dataset, i_forecast_dataset, forecast_json):
    threshold = float(Runtime().ENV['forecast.threshold.' + instance])
    # 自编码器预测
    param_dict = paddle.load(
        cfg().HOME + '/src/model/' + instance + '.md')  # 读取保存的参数
    a_index = auto_encoder_forecast(instance, a_forecast_dataset, param_dict, threshold)
    # 孤立森林预测
    with open(cfg().HOME + '/src/model/' + instance + '.if',
              'r') as load_f:
        json_tree_if = json.load(load_f)
        i_index = iforest_forecast(instance, i_forecast_dataset, json_tree_if)
    # 集合整理
    a_subset, i_subset, u_subset = subset(forecast_json, a_index, i_index)
    # 保存进数据库
    db(instance, forecast_json, a_subset, i_subset, u_subset)
    # 画图
    draw(instance, forecast_json, a_subset, i_subset, u_subset)


def auto_encoder_forecast(instance, forecast_dataset, param_dict, threshold):
    model = AutoEncoder()
    model.load_dict(param_dict)  # 加载参数
    model.eval()  # 预测
    mse_loss = paddle.nn.loss.MSELoss()
    x = paddle.to_tensor(forecast_dataset.data).astype('float32')
    abnormal_index = []  # 记录检测到异常时数据的索引
    for i in range(len(forecast_dataset)):
        input_x = paddle.reshape(x[i], (1, 1, int(Runtime().ENV['dataset.time.step'])))
        out = model(input_x)
        loss = mse_loss(input_x[:, :, :-1], out)
        if loss.numpy()[0] > threshold:
            # 开始检测到异常时序列末端靠近异常点，所以要加上序列长度，得到真实索引位置
            abnormal_index.append(i + int(Runtime().ENV['dataset.time.step']))
        # if i % 100 == 0 and instance == '172.18.48.213':
        #     input_x = paddle.reshape(x[i], (1, 1, int(Runtime().ENV['dataset.time.step'])))
        #     out = model(input_x)
        #     loss = mse_loss(input_x[:, :, :-1], out)
        #     plt.figure(figsize=(20, 4))
        #     plt.ylim(0, 10)
        #     plt.margins(x=0)
        #     plt.grid(True)
        #     plt.grid(linestyle='dotted', c='silver', axis="both")
        #     ax = plt.subplot()
        #     ax.set_ylim(0, 10)
        #     ax.margins(x=0)
        #     plt.plot(range(719), input_x[0, 0, :-1].numpy(), color='silver')
        #     plt.plot(range(719), out[0, 0].numpy(), color='pink')
        #     path = cfg().HOME + "/src/result/see/" + instance + "/"
        #     isExists = os.path.exists(path)
        #     if not isExists:
        #         os.makedirs(path)
        #     plt.savefig(path + str(i) + ".png", dpi=160,
        #                 bbox_inches='tight')
        #     plt.cla()
        #     plt.close()
        #     if loss.numpy()[0] > threshold:
        #         # 开始检测到异常时序列末端靠近异常点，所以要加上序列长度，得到真实索引位置
        #         abnormal_index.append(i + int(Runtime().ENV['dataset.time.step']))
    return abnormal_index


def iforest_forecast(instance, i_forecast_dataset, json_tree_if):
    index = []
    for data in enumerate(i_forecast_dataset):
        sum_data = 0
        for t in json_tree_if:
            score = forecast_in_tree(data, t, 0)
            sum_data += score
        avf_data = sum_data / len(json_tree_if)
        s = math.pow(2, -(avf_data / c_equation(len(i_forecast_dataset))))
        record = float(Runtime().ENV['forecast.iforest.' + instance])
        if s > record:
            index.append(data[0])
    return index


def forecast_in_tree(x, t, e):
    if 'size' in t:
        return e + c_equation(int(t['size']))
    else:
        if float(x[1][1]) < float(t['split_value']):
            return forecast_in_tree(x, t['left'], e + 1)
        elif float(x[1][1]) >= float(t['split_value']):
            return forecast_in_tree(x, t['right'], e + 1)


def c_equation(n):
    if n > 1:
        return 2 * h_equation(n - 1) - (2 * (n - 1) / n)
    else:
        return 0


def h_equation(n):
    return math.log(n) + ξ


def subset(forecast_json, a_index, i_index):
    a_index = [x - int(Runtime().ENV['dataset.time.step']) for x in a_index]
    a_subset = forecast_json.iloc[a_index]
    i_subset = forecast_json.iloc[i_index]
    u_list = list(set(a_index).intersection(set(i_index)))
    u_list.sort()
    u_subset = forecast_json.iloc[u_list]
    return a_subset, i_subset, u_subset


def db(instance, o_subset, a_subset, i_subset, u_subset):
    session = DB().get_session()()
    res = Result(
        id=str(uuid.uuid1()),
        instance=instance,
        origin_index=o_subset.to_json(orient='split', force_ascii=False),
        auto_index=a_subset.to_json(orient='split', force_ascii=False),
        iforest_index=i_subset.to_json(orient='split', force_ascii=False),
        merge_index=u_subset.to_json(orient='split', force_ascii=False))
    session.add(res)
    session.commit()
    session.close()


def draw(instance, o_subset, a_subset, i_subset, u_subset):
    print(instance)
    plt.figure(figsize=(200, 4))
    plt.ylim(0, 100)
    plt.margins(x=0)
    plt.grid(True)
    plt.grid(linestyle='dotted', c='silver', axis="both")
    ax = plt.subplot()
    # fig.set_size_inches(200, 4)
    ax.set_title(instance)
    ax.set_ylim(0, 100)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(dates.MinuteLocator(byminute=range(60), interval=30))
    ax.xaxis.set_major_formatter(
        dates.DateFormatter('%H:%M:%S', tz=tzoffset(name='UTC+8', offset=timedelta(hours=8))))
    plt.plot(o_subset['precent'].keys(), o_subset['precent'].values, color='silver', linewidth=1,
             label='origin')
    plt.plot(a_subset['precent'].keys(), a_subset['precent'].values, color='b', linewidth=1,
             label='auto')
    plt.plot(i_subset['precent'].keys(), i_subset['precent'].values, color='g', linewidth=1,
             label='iforest')
    plt.plot(u_subset['precent'].keys(), u_subset['precent'].values, color='r', linewidth=1,
             label='union')
    date = time.strftime("%Y-%m-%d", time.localtime())
    path = cfg().HOME + "/src/result/" + date + "/"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    plt.savefig(path + instance + ".png", dpi=160,
                bbox_inches='tight')
    print(instance, "image save finish")
