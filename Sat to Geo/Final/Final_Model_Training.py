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
from datasets import *

import torch.nn as nn
import torch.nn.functional as F
import torch

parser = argparse.ArgumentParser()
parser.add_argument("--epoch", type=int, default=0, help="epoch to start training from")
parser.add_argument("--n_epochs", type=int, default=10, help="number of epochs of training")
parser.add_argument("--dataset_name", type=str, default="Split_Images_DM", help="name of the dataset")
parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
parser.add_argument("--lr", type=float, default=0.0002, help="adam: learning rate")
parser.add_argument("--b1", type=float, default=0.5, help="adam: decay of first order momentum of gradient")
parser.add_argument("--b2", type=float, default=0.999, help="adam: decay of first order momentum of gradient")
parser.add_argument("--decay_epoch", type=int, default=100, help="epoch from which to start lr decay")
parser.add_argument("--n_cpu", type=int, default=2, help="number of cpu threads to use during batch generation")
parser.add_argument("--img_height", type=int, default=256, help="size of image height")
parser.add_argument("--img_width", type=int, default=256, help="size of image width")
parser.add_argument("--channels", type=int, default=3, help="number of image channels")
parser.add_argument(
    "--sample_interval", type=int, default=500, help="interval between sampling of images from generators"
)
parser.add_argument("--checkpoint_interval", type=int, default=50, help="interval between model checkpoints")
parser.add_argument("--src_path", type=str, default="temporary", help="path where the generated training data is stored")
parser.add_argument("--save_path", type=str, default="temporary", help="path where images and models will be saved to")
opt = parser.parse_args()

if opt.src_path == "temporary" or opt.save_path == "temporary":
    raise Exception("Sorry, either src_path, save_path, or model_path was not given.")

os.makedirs("%s/images_sprint_2" % (opt.save_path), exist_ok=True)
os.makedirs("%s/saved_models_sprint_2" % (opt.save_path), exist_ok=True)
os.makedirs("%s/Log_Reports" % (opt.save_path), exist_ok=True)

os.makedirs("%s/images_sprint_2/%s" % (opt.save_path, opt.dataset_name), exist_ok=True)
os.makedirs("%s/saved_models_sprint_2/%s" % (opt.save_path, opt.dataset_name), exist_ok=True)

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

# Initialize weights
generator.apply(weights_init_normal)
discriminator.apply(weights_init_normal)

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

# Configure dataloaders
transforms_ = [
    transforms.Resize((opt.img_height, opt.img_width), Image.BICUBIC),
    transforms.ToTensor(),
    #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
]

dataloader = DataLoader(
    ImageDataset("%s/%s" % (opt.src_path, opt.dataset_name), transforms_=transforms_),
    batch_size=opt.batch_size,
    shuffle=True,
    num_workers=opt.n_cpu,
)

val_dataloader = DataLoader(
    ImageDataset("%s/%s" % (opt.src_path, opt.dataset_name), transforms_=transforms_, mode="val"),
    batch_size=10,
    shuffle=True,
    num_workers=1,
)

# Tensor type
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor


def sample_images(batches_done):
    """Saves a generated sample from the validation set"""
    imgs = next(iter(val_dataloader))
    real_A = Variable(imgs["B"].type(Tensor))
    real_B = Variable(imgs["A"].type(Tensor))
    fake_B = generator(real_A)
    img_sample = torch.cat((real_A.data, fake_B.data, real_B.data), -2)
    save_image(img_sample, "%s/images_sprint_2/%s/%s.png" % (opt.save_path, opt.dataset_name, batches_done), nrow=5, normalize=True)

# ----------
#  Training
# ----------

prev_time = time.time()

if __name__ == "__main__":
    print(cuda)

    f = open("%s/Log_Reports/training_log.txt" % (opt.save_path), "w")

    for epoch in range(opt.epoch, opt.n_epochs):
        for i, batch in enumerate(dataloader):

            # Model inputs
            real_A = Variable(batch["B"].type(Tensor))
            real_B = Variable(batch["A"].type(Tensor))

            new_size = (real_A.size(0), patch[0], patch[1], patch[2])

            # Adversarial ground truths
            valid = Variable(Tensor(np.ones(new_size)), requires_grad=False)
            fake = Variable(Tensor(np.zeros(new_size)), requires_grad=False)

            # ------------------
            #  Train Generators
            # ------------------

            optimizer_G.zero_grad()

            # GAN loss
            fake_B = generator(real_A)
            pred_fake = discriminator(fake_B, real_A)
            loss_GAN = criterion_GAN(pred_fake, valid)
            # Pixel-wise loss
            loss_pixel = criterion_pixelwise(fake_B, real_B)

            # Total loss
            loss_G = loss_GAN + lambda_pixel * loss_pixel

            loss_G.backward()

            optimizer_G.step()

            # ---------------------
            #  Train Discriminator
            # ---------------------

            optimizer_D.zero_grad()

            # Real loss
            pred_real = discriminator(real_B, real_A)
            loss_real = criterion_GAN(pred_real, valid)

            # Fake loss
            pred_fake = discriminator(fake_B.detach(), real_A)
            loss_fake = criterion_GAN(pred_fake, fake)

            # Total loss
            loss_D = 0.5 * (loss_real + loss_fake)

            loss_D.backward()
            optimizer_D.step()

            # --------------
            #  Log Progress
            # --------------

            # Determine approximate time left
            batches_done = epoch * len(dataloader) + i
            batches_left = opt.n_epochs * len(dataloader) - batches_done
            time_left = datetime.timedelta(seconds=batches_left * (time.time() - prev_time))
            prev_time = time.time()

            # Print log
            sys.stdout.write(
                "\r[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f, pixel: %f, adv: %f] ETA: %s"
                % (
                    epoch,
                    opt.n_epochs,
                    i,
                    len(dataloader),
                    loss_D.item(),
                    loss_G.item(),
                    loss_pixel.item(),
                    loss_GAN.item(),
                    time_left,
                )
            )

            f.write("%f %f %f %f\n" % (loss_D.item(), loss_G.item(), loss_pixel.item(), loss_GAN.item()))

            # If at sample interval save image
            if batches_done % opt.sample_interval == 0:
                sample_images(batches_done)

        if opt.checkpoint_interval != -1 and epoch % opt.checkpoint_interval == 0:

            print("\nSaved model")

            # Save model checkpoints
            torch.save(generator.state_dict(), "%s/saved_models_sprint_2/%s/generator_v2_%d.pth" % (opt.model_path, opt.dataset_name, epoch))
            torch.save(discriminator.state_dict(), "%s/saved_models_sprint_2/%s/discriminator_v2_%d.pth" % (opt.model_path, opt.dataset_name, epoch))

    # Final Image
    sample_images("Final")

    torch.save(generator.state_dict(), "%s/saved_models_sprint_2/%s/generator_%s.pth" % (opt.model_path, opt.dataset_name, opt.dataset_name))
    torch.save(discriminator.state_dict(), "%s/saved_models_sprint_2/%s/discriminator_%s.pth" % (opt.model_path, opt.dataset_name, opt.dataset_name))
    f.close()
