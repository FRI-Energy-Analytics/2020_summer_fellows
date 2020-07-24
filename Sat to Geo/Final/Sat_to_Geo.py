import argparse
import os
import numpy as np
import math
import itertools
import time
import datetime
import sys

import torchvision.transforms as transforms
from torchvision.utils import save_image

from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

from models import *
from datasets_loader import *

import torch.nn as nn
import torch.nn.functional as F
import torch

parser = argparse.ArgumentParser()
parser.add_argument("--lr", type=float, default=0.0002, help="adam: learning rate")
parser.add_argument("--b1", type=float, default=0.5, help="adam: decay of first order momentum of gradient")
parser.add_argument("--b2", type=float, default=0.999, help="adam: decay of first order momentum of gradient")
parser.add_argument("--img_height", type=int, default=256, help="size of image height")
parser.add_argument("--img_width", type=int, default=256, help="size of image width")
parser.add_argument("--src_path", type=str, default="temporary", help="path where the generated training data is stored")
parser.add_argument("--save_path", type=str, default="temporary", help="path where images and models will be saved to")
parser.add_argument("--gen_path", type=str, default="temporary", help="path to the geneorator model to load in")
parser.add_argument("--dis_path", type=str, default="temporary", help="path to the discriminator model to load in")
opt = parser.parse_args()

if (opt.src_path == "temporary" or opt.save_path == "temporary" or opt.gen_path == "temporary" or opt.dis_path == "temporary"):
    raise Exception("Either src_path, save_path, gen_path or dis_path was not provided")


cuda = True if torch.cuda.is_available() else False

# Loss functions
criterion_GAN = torch.nn.MSELoss()
criterion_pixelwise = torch.nn.L1Loss()

# Loss weight of L1 pixel-wise loss between translated image and real image
lambda_pixel = 100

# Calculate output of image discriminator (PatchGAN)
patch = (1, opt.img_height // 2 ** 4, opt.img_width // 2 ** 4)

# Initialize generator and discriminator
generator = GeneratorUNet()
discriminator = Discriminator()

if cuda:
    generator = generator.cuda()
    discriminator = discriminator.cuda()
    criterion_GAN.cuda()
    criterion_pixelwise.cuda()

generator.load_state_dict(torch.load("%s" % (opt.gen_path)))
discriminator.load_state_dict(torch.load("%s" % (opt.dis_path)))

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

# Configure dataloaders
transforms_ = [
    transforms.Resize((opt.img_height, opt.img_width), Image.BICUBIC),
    transforms.ToTensor(),
    #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
]

val_dataloader = DataLoader(
    ImageDataset("%s" % (opt.src_path), transforms_=transforms_, mode="imgs"),
    batch_size=10,
    shuffle=False,
    num_workers=1,
)

# Tensor type
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor


def sample_images(batches_done, imgs):
    """Saves a generated sample from the validation set"""
    real_A = Variable(imgs["B"].type(Tensor))
    fake_B = generator(real_A)
    img_sample = torch.cat((real_A.data, fake_B.data), -2)
    save_image(img_sample, "%s/%s.png" % (opt.save_path, batches_done), nrow=2, normalize=True)

# ----------
#  Training
# ----------

prev_time = time.time()

if __name__ == "__main__":

    i = 0
    for batch in val_dataloader:
        sample_images(i, batch)
        i += 1


    # imgs = next(iter(val_dataloader))
    # real_A = Variable(imgs["B"].type(Tensor))
    # real_B = Variable(imgs["A"].type(Tensor))
    # fake_B = generator(real_A)
    # img_sample = torch.cat((real_A.data, fake_B.data, real_B.data), -2)
    # save_image(img_sample, "%s/%s.png" % (opt.save_path, "Testing"), nrow=5, normalize=True)
