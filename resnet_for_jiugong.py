import torch
import torchvision.models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.autograd import Variable

model_lr = 1e-4
BATCH_SIZE = 64
EPOCHS = 20
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 数据预处理

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

])
transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# 读取数据
dataset_train = datasets.ImageFolder('data/train', transform)
print(dataset_train.imgs)
# 对应文件夹的label
print(dataset_train.class_to_idx)
dataset_test = datasets.ImageFolder('data/val', transform_test)
# 对应文件夹的label
print(dataset_test.class_to_idx)

# 导入数据
train_loader = DataLoader(dataset_train, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(dataset_test, batch_size=BATCH_SIZE, shuffle=False)

# build model, loss and optimizer
resnet50 = torchvision.models.resnet18(pretrained=True)
optimizer = torch.optim.Adam(resnet50.parameters(), lr=model_lr)
criterion = nn.CrossEntropyLoss()

num_features = resnet50.fc.in_features
resnet50.fc = nn.Linear(num_features, 2)
resnet50.train()


def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    model_lr_new = model_lr * (0.1 ** (epoch // 50))
    print("lr:", model_lr_new)
    for param_group in optimizer.param_groups:
        param_group['lr'] = model_lr_new


# 定义训练过程

def train(model, device, train_loader, optimizer, epoch):
    model.train()
    sum_loss = 0
    total_num = len(train_loader.dataset)
    print(total_num, len(train_loader))
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data).to(device), Variable(target).to(device)
        output = model(data)
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print_loss = loss.data.item()
        sum_loss += print_loss
        if (batch_idx + 1) % 50 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, (batch_idx + 1) * len(data), len(train_loader.dataset),
                       100. * (batch_idx + 1) / len(train_loader), loss.item()))
    ave_loss = sum_loss / len(train_loader)
    print('epoch:{},loss:{}'.format(epoch, ave_loss))


def val(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    total_num = len(test_loader.dataset)
    print(total_num, len(test_loader))
    with torch.no_grad():
        for data, target in test_loader:
            data, target = Variable(data).to(device), Variable(target).to(device)
            output = model(data)
            loss = criterion(output, target)
            _, pred = torch.max(output.data, 1)
            correct += torch.sum(pred == target)
            print_loss = loss.data.item()
            test_loss += print_loss
        correct = correct.data.item()
        acc = correct / total_num
        avgloss = test_loss / len(test_loader)
        print('\nVal set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            avgloss, correct, len(test_loader.dataset), 100 * acc))


# 训练

for epoch in range(1, EPOCHS + 1):
    adjust_learning_rate(optimizer, epoch)
    train(resnet50, DEVICE, train_loader, optimizer, epoch)
    val(resnet50, DEVICE, test_loader)
torch.save(resnet50, 'model.pth')
