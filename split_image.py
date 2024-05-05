import torch
from torchvision import transforms
from torchvision.utils import save_image
from dataset import Pix2PixDataset
from torch_snippets import DataLoader
import cv2
import matplotlib.pyplot as plt
from torch_snippets import *

IMAGE_SIZE = 256
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

denorm = transforms.Normalize((-1, -1, -1), (2, 2, 2))

val_ds = Pix2PixDataset('data\edges2shoes\\val')
val_dl = DataLoader(val_ds, 1, shuffle=True, collate_fn=val_ds.collate_fn)

for index, images in enumerate(val_dl):
    # if index==0:
    real_src, real_tgt = images
    real_src.squeeze_(0), real_tgt.squeeze_(0)
    print(real_src.shape, real_tgt.shape)
    # img_sample = torch.cat([denorm(real_src[0]), denorm(real_tgt[0])], -1)
    # print(img_sample.shape)
    # # print(real_src.shape)
    save_image(denorm(real_src),f'data\edges2shoes\\for_web\{index}.jpg')
    # show(real_src.detach().cpu().permute(1,2,0).numpy())
    # plt.im