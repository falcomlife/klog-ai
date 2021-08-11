import paddle.nn.functional as F
import paddle

class AutoEncoder(paddle.nn.Layer):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.conv0 = paddle.nn.Conv1D(in_channels=1,out_channels=32,kernel_size=7,stride=2)
        self.conv1 = paddle.nn.Conv1D(in_channels=32,out_channels=16,kernel_size=7,stride=2)
        self.convT0 = paddle.nn.Conv1DTranspose(in_channels=16,out_channels=32,kernel_size=7,stride=2)
        self.convT1 = paddle.nn.Conv1DTranspose(in_channels=32,out_channels=1,kernel_size=7,stride=2)

    def forward(self, x):
        x = self.conv0(x)
        x = F.relu(x)
        x = F.dropout(x,0.2)
        x = self.conv1(x)
        x = F.relu(x)
        x = self.convT0(x)
        x = F.relu(x)
        x = F.dropout(x,0.2)
        x = self.convT1(x)
        return x