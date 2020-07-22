import glob
import random
import os
import numpy as np
import cv2
from scipy import ndimage, misc

InFolder = "/Users/ashwanthmuruhathasan/Documents/GitHub/summer_fellows/Sat to Geo/Sprint 1/Collected_Images/Split_Images"
OutFolder = "/Users/ashwanthmuruhathasan/Documents/GitHub/summer_fellows/Sat to Geo/Sprint 2/NoiseDetection/NoiseImages"
FolderTypes = ["test", "train", "val"]
# noiseTypes = ["gauss", "s&p", "poisson", "speckle", "perlin"]
noiseTypes = ["sgs"]
perlinLoc = "perlin_1.png"
sgsLoc = "sgs_1.png"
gw, gh = 256, 256

def noisy(noise_typ,image):
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss
        return noisy
    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        out[coords] = 1
        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)
        noisy = image + image * gauss
        return noisy
    elif noise_typ == "perlin":
        noisy = cv2.imread(os.path.join(OutFolder, perlinLoc))
        return noisy
    elif noise_typ == "sgs":
        noisy = cv2.imread(os.path.join(OutFolder, sgsLoc))
        return noisy

def getBlankNoiseImg(w, h, noise_typ):
    blank = 0 * np.ones(shape=[h, w, 3], dtype=np.uint8)
    noiseImg = noisy(noise_typ, blank)
    return noiseImg

def shiftImg(img):
    h, w, c = img.shape
    xshift = random.randint(0,w)
    yshift = random.randint(0,h)
    shifted = np.zeros(shape=[h, w, 3], dtype=np.uint8)
    for x in range(0,w):
        for y in range(0,h):
            shifted[y,x] = img[(y+yshift)%h,(x+xshift)%w]
    return shifted

def processFolder(inpath, outpath, modImg):
    for image_path in os.listdir(inpath):
        fullinpath = os.path.join(inpath, image_path)
        image = cv2.imread(fullinpath)
        h, w, c = image.shape
        cropImg = image[0:h,0:w//2]
        
        # mod here
        shiftedmodImg = shiftImg(modImg)
        combImg = cv2.addWeighted(cropImg, 0.2, shiftedmodImg, 0.8, 0)
        finImg = np.concatenate((cropImg, combImg), axis=1)
        
        fulloutpath = os.path.join(outpath, image_path)
        status = cv2.imwrite(fulloutpath, finImg)
        # print("Image written to file-system : ",status)
        
    return "fin"
    
def processDataset(inpath, outpath, noise_typ):
    newFolder = os.path.join(outpath, noise_typ)
    os.mkdir(newFolder)
    
    # get image
    noisyImg = getBlankNoiseImg(gw, gh, noise_typ)
    
    for foldername in FolderTypes:
        ninpath = os.path.join(inpath, foldername)
        noutpath = os.path.join(newFolder, foldername)
        os.mkdir(noutpath)
        processFolder(ninpath, noutpath, noisyImg)
        
    return "fin"

def process():
    for noisetype in noiseTypes:
        processDataset(InFolder, OutFolder, noisetype)
    return "fin"
    
process()
