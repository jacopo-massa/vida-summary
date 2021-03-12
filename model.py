import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable as V

from config import *


def read_img(filename):
    img = get_image(filename)

    transform = transforms.Compose([transforms.Resize([224, 224]),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    x = transform(img)
    x = x.unsqueeze(0)
    return x


# 2D CNN encoder using ResNet-50 pretrained

class VidaResNet(nn.Module):
    def __init__(self, in_size=1, out_size=1):
        """Load the pretrained ResNet-50 and replace top fc layer."""
        super(VidaResNet, self).__init__()

        resnet = models.resnet50(pretrained=True)

        for param in resnet.parameters():
            param.requires_grad = False

        modules = list(resnet.children())[:-1]  # delete the last fc layer.
        self.resnet = nn.Sequential(*modules)
        self.eval()

    def forward(self, input):
        # ResNet CNN
        with torch.no_grad():
            x = self.resnet(input)  # ResNet
            x = x.view(x.size(0), -1)  # flatten output of conv

        return x

    def predict(self, filename):
        stim = read_img(filename)

        with torch.no_grad():
            if torch.cuda.is_available():
                stim = V(stim.cuda())
            else:
                stim = V(stim)
            out = self.resnet(stim)

        return out
