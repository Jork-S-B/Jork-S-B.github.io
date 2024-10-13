深度神经网络，通过构建多层人工神经网络模拟人类大脑的信息处理和学习机制，实现对大量数据的处理和分析。

pytorch，用于构建和训练深度神经网络的工具。

## 📌 范式周期

### 📍 准备数据

准备数据，将数据转为适合神经网络模型训练的数据。

1. 数据下载，pytorch提供加载和下载数据集的功能
2. 数据格式转换，ToTensor()预处理，将PIL图像转为PytorchTensor图像，并调整精度
3. 数据集划分，分为多个批次+枚举方式训练

```python
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from pathlib import Path

# 定义保存或加载数据集的位置
# path = '~/.torch/datasets/mnist'

path = Path(".") / ".torch" / "datasets" / "mnist"

# 下载并定义数据集
train = MNIST(path, train=True, download=True, transform=ToTensor())
test = MNIST(path, train=False, download=True, transform=ToTensor())

# 数据集划分
from torch.utils.data import DataLoader

train_dl = DataLoader(train, batch_size=64, shuffle=True)
test_dl = DataLoader(test, batch_size=1024, shuffle=False)

print("总数据集数量为：", len(train))  # 60000
print("每批训练数据集数量为：", len(train_dl))  # 60000/64=938

from matplotlib import pyplot

# 枚举并绘图
i, (inputs, targets) = next(enumerate(train_dl))
for i in range(25):
    # 在5x5的网格中绘制每个样本的灰度图像
    # 灰度图像：每个像素用不同深浅的灰色表示，而不包含颜色信息。
    pyplot.subplot(5, 5, i + 1)
    # 绘制原始像素数据
    pyplot.imshow(inputs[i][0], cmap='gray')
# 展示图片
pyplot.show()

```

### 📍 定义模型

* 卷积层：转换为0-1的数据矩阵，减少参数数量。
* 池化层：对卷积层输出的特征图进行下采样，减少数据维度。
* 全连接层：分类结果，通过加权求和得到每个类别的得分。

### 📍 训练模型

输入训练数据，计算损失调整参数并重复多个周期，直至模型学到训练数据的特征。

损失函数，衡量模型预测的准确性
优化器，用于调整模型的参数

### 📍 评估模型

### 📍 做出预测
