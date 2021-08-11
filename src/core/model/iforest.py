import math
import random

import numpy as np

class IForest:

    def __init__(self):
        super(IForest, self).__init__()
        self.forest = []

    def iforest(self, datas, tree_num, sub_sample_size):
        limit_height = math.ceil(math.log(sub_sample_size, 2))
        for index in range(tree_num):
            index_np = list(range(0, len(datas)))
            random.shuffle(index_np)
            samples_index = index_np[0:sub_sample_size]
            samples = datas[[samples_index]]
            self.forest.append(self.itree(samples, 0, limit_height))
            print(index, " tree has finished")
        return self.forest

    def itree(self, data, current_heigit, limit_height):
        # 考虑最后可能有好几个一样的值，这里用"1 == len(set(list(data[:, 1].reshape(len(data)))))"
        if current_heigit >= limit_height or len(data) <= 1 or 1 == len(set(list(data[:, 1].reshape(len(data))))):
            return {"size": len(data)}
        else:
            max_value = max(list(data[:, 1]))
            min_value = min(list(data[:, 1]))
            p = random.uniform(float(min_value), float(max_value))
            index_left = np.argwhere(data[:, 1].astype('float64') < p)
            index_right = np.argwhere(data[:, 1].astype('float64') >= p)
            return {
                "left": IForest().itree(data[index_left.reshape(len(index_left))], current_heigit + 1, limit_height),
                "right": IForest().itree(data[index_right.reshape(len(index_right))], current_heigit + 1,
                                         limit_height),
                "split_att": None,
                "split_value": p
            }
