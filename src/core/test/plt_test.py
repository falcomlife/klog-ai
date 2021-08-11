import datetime
import json
import math

import pandas as pd
from matplotlib import pyplot as plt
from data.pretreatment import read_train_data, read_forecast_data

# for instance, data in read_train_data().items():
#     train_json = pd.read_json(json.dumps(data), orient='split')
#     ax = plt.subplot()
#     train_json.plot(legend=False, ax=ax)
#     ax.set_title(instance)
# i = 1
# for instance, data in read_forecast_data().items():
#     if instance == '172.16.7.133':
#         for ii, num in enumerate(data['data']):
#             if float(num[0]) > 15:
#                 print(str(data['index'][ii]) + ':' + num[0])
#     train_json = pd.read_json(json.dumps(data), orient='split')
#     ax = plt.subplot(4, 1, i)
#     train_json.plot(legend=False, ax=ax)
#     ax.set_title(instance)
#     i += 1
# plt.figure(figsize=(40, 8))
#
# x = [1, 2, 3]
# plt.plot(x, x)
# plt.show()
# print(math.log(3000,2))
