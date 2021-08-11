import json
import tqdm
import paddle
import numpy as np

from common.args import Runtime
from model.auto_encoder import AutoEncoder
from matplotlib import pyplot as plt

from model.iforest import IForest
from common.config import config as cfg

EPOCH_NUM = int(Runtime().ENV['model.auto.epoch.num'])
BATCH_SIZE = int(Runtime().ENV['model.auto.batch.size'])
LEARNING_RATE = float(Runtime().ENV['model.auto.learning.rate'])


# 训练步骤
def train(instance, train_dataset, train_datas, *args):
    # 进行自编码器的训练
    if 'auto' in args:
        auto_envoder(instance, train_dataset)
    # 进行孤立树训练
    if 'iforest' in args:
        iforest(instance, train_datas)


# 计算自编码器的阈值
def valid(instance, train_dataset):
    # 计算阀值
    param_dict = paddle.load(
        cfg().HOME + '/src/model/' + instance + '.md')  # 读取保存的参数
    model = AutoEncoder()
    model.load_dict(param_dict)  # 加载参数
    model.eval()  # 预测
    total_loss = []
    datas = []
    # 预测所有正常时序
    mse_loss = paddle.nn.loss.MSELoss()
    # 这里设置batch_size为1，单独求得每个数据的loss
    data_reader = paddle.io.DataLoader(train_dataset,
                                       places=[paddle.CPUPlace()],
                                       batch_size=1,
                                       shuffle=False,
                                       drop_last=False,
                                       num_workers=0)
    for batch_id, data in enumerate(data_reader()):
        x = data[0]
        y = data[1]
        out = model(x)
        avg_loss = mse_loss(out, (y[:, :, :-1]))
        total_loss.append(avg_loss.numpy()[0])
        datas.append(batch_id)

    # 获取重建loss的阀值
    threshold = np.max(total_loss)
    print(instance, " 阀值:", threshold)


# 查看子编码器效果
def see(instance, train_dataset):
    import sys
    param_dict = paddle.load(
        cfg().HOME + '/src/model/' + instance + '.md')  # 读取保存的参数
    model = AutoEncoder()
    model.load_dict(param_dict)  # 加载参数
    model.eval()  # 预测
    data_reader = paddle.io.DataLoader(train_dataset,
                                       places=[paddle.CPUPlace()],
                                       batch_size=128,
                                       shuffle=False,
                                       drop_last=False,
                                       num_workers=0)
    for batch_id, data in enumerate(data_reader()):
        x = data[0]
        out = model(x)
        step = np.arange(1439)
        # plt.title(instance)
        # plt.plot(step, x[0, 0, :-1].numpy())
        # plt.plot(step, out[0, 0].numpy())
        # plt.show()
        sys.exit


def auto_envoder(instance, train_dataset):
    print('训练开始')
    # 实例化模型
    model = AutoEncoder()
    # 将模型转换为训练模式
    model.train()
    # 设置优化器，学习率，并且把模型参数给优化器
    opt = paddle.optimizer.Adam(learning_rate=LEARNING_RATE, parameters=model.parameters())
    # 设置损失函数
    mse_loss = paddle.nn.MSELoss()
    # 设置数据读取器
    data_reader = paddle.io.DataLoader(train_dataset,
                                       batch_size=BATCH_SIZE,
                                       shuffle=True,
                                       drop_last=True)
    history_loss = []
    iter_epoch = []
    for epoch in tqdm.tqdm(range(EPOCH_NUM)):
        for batch_id, data in enumerate(data_reader()):
            x = data[0]
            y = data[1]
            out = model(x)
            avg_loss = mse_loss(out, (y[:, :, :-1]))  # 输入的数据经过卷积会丢掉最后一个数据
            avg_loss.backward()
            opt.step()
            opt.clear_grad()
        iter_epoch.append(epoch)
        history_loss.append(avg_loss.numpy()[0])
    # 绘制loss
    # plt.plot(iter_epoch, history_loss, label='loss')
    # plt.legend()
    # plt.xlabel('iters')
    # plt.ylabel('Loss')
    # plt.show()
    # 保存模型参数
    paddle.save(model.state_dict(),
                cfg().HOME + '/src/model/' + instance + '.md')


def iforest(instance, train_datas):
    iforest = IForest().iforest(train_datas, tree_num=200, sub_sample_size=200)
    # _thread.start_new_thread(write_tree, (iforest, instance))
    write_tree(iforest, instance)


def write_tree(iforest, instance):
    with open(cfg().HOME + '/src/model/' + instance + '.if',
              mode='w') as f:
        json.dump(iforest, f)
