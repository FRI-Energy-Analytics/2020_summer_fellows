## Sat To Geo pix2pix GAN Training Instructions

### Notes
  * CUDA support optional (requires Nvidia GPU)

### Run GAN
```
git clone https://github.com/eriklindernoren/PyTorch-GAN
cd Pytorch-GAN/
Sudo pip3 install -r requirements

# move SatToGeo dataset into data/

cd implementations/pix2pix
python3 pix2pix.py —dataset_name SatToGeo

# images/ saves testing output
# saved_models/ saves generator and discriminator
```
