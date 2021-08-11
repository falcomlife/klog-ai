import paddle
import numpy as np

class Dataset(paddle.io.Dataset):
    """
    步骤一：继承paddle.io.Dataset类
    """
    def __init__(self,data,time_steps):
        """
        步骤二：实现构造函数，定义数据读取方式，划分训练和测试数据集
        注意：这个是不需要label
        """
        super(Dataset, self).__init__()
        self.time_steps = int(time_steps)
        self.data = paddle.to_tensor(self.transform(data), dtype='float32')

    def transform(self,data):
        '''
        构造时序数据
        '''
        output = []
        for i in range(len(data) - self.time_steps):
            output.append(np.reshape(data[i : (i + self.time_steps)], (1,self.time_steps)))
        return np.stack(output)

    def __getitem__(self, index):
        """
        步骤三：实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据）
        """
        data = self.data[index]
        label = self.data[index]
        return data, label

    def __len__(self):
        """
        步骤四：实现__len__方法，返回数据集总数目
        """
        return len(self.data)
