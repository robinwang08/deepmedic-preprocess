from __future__ import division
import os
import nibabel as nib
import numpy as np
from glob import glob

def getMax():
    mainPath = 'C:/Users/Robin/Downloads/raw1/raw1'
    mttMax = 0
    labelMax = 0

    baseDir = os.path.normpath(mainPath)
    imagefiles = glob(baseDir + '/*/T1POST/imagingVolume-resampled.nii')
    maskfiles = glob(baseDir + '/*/T1POST/segMask_tumor-resampled.nii')

    for file in imagefiles:
        n1_img = nib.load(file)
        img = n1_img.get_fdata()
        imgmax = img.max()
        if imgmax > mttMax:
            mttMax = imgmax

    for file in maskfiles:
        n1_img = nib.load(file)
        img = n1_img.get_fdata()
        imgmax = img.max()
        if imgmax > labelMax:
            labelMax = imgmax

    f = open('C:/Users/Robin/Downloads/ctnormalize.txt','a+')
    f.write('MTT: ' + str(mttMax) + '\n')
    f.write('label: ' + str(labelMax) + '\n')
    return

def normalize():
    mainPath = 'C:/Users/Robin/Downloads/test'
    newPath = 'C:/Users/Robin/Downloads/test2'

    mttMax = 1177.0

    baseDir = os.path.normpath(mainPath)
    imagefiles = glob(baseDir + '/*/T1POST/imagingVolume-resampled.nii')


    for file in imagefiles:
        n1_img = nib.load(file)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        img = np.true_divide(img, mttMax)
        new_img = nib.Nifti1Image(img, n1_affine, n1_header)

        filePath, fileName = os.path.split(file)
        a = filePath.split('\\')

        nePath = newPath + '/' + a[5]
        neePath = nePath + '/T1POST'
        newwPath = neePath + '/' + fileName

        if not os.path.isdir(nePath):
            os.mkdir(nePath)

        if not os.path.isdir(neePath):
            os.mkdir(neePath)

        nib.save(new_img, newwPath)


    for x in range(2, 228):
        path = mainPath + str(x)
        normPath = newPath + str(x)

        MTT = path + '/MTT.nii'
        newMTT = normPath + '/MTT.nii'

        if not os.path.exists(MTT):
            continue

        if not os.path.exists(normPath):
            os.mkdir(normPath)


def getROI():
    mainPath = 'F:/Research/data/padded/'
    newPath = 'F:/Research/data/padded/'

    for x in range(2, 228):
        path = mainPath + str(x)
        normPath = newPath + str(x)

        MTT = path + '/MTT.nii'
        newMTT = normPath + '/mask.nii'

        if not os.path.exists(MTT):
            continue

        if not os.path.exists(normPath):
            os.mkdir(normPath)

        n1_img = nib.load(MTT)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        img[img > 0] = 1

        new_img = nib.Nifti1Image(img, n1_affine, n1_header)
        nib.save(new_img, newMTT)


def getPad():
    mainPath = 'F:/Research/data/normalized/'
    newPath = 'F:/Research/data/padded/'

    for x in range(2, 228):
        path = mainPath + str(x)
        normPath = newPath + str(x)
        MTT = path + '/MTT.nii'
        newMTT = normPath + '/MTT.nii'
        if not os.path.exists(MTT):
            continue
        if not os.path.exists(normPath):
            os.mkdir(normPath)

        n1_img = nib.load(MTT)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        # add padding
        padded = np.pad(img, ((0, 0), (0, 0), (18, 18)), 'constant', constant_values=(0, 0))
        new_img = nib.Nifti1Image(padded, n1_affine, n1_header)
        nib.save(new_img, newMTT)

        rCBF = path + '/rCBF.nii'
        newrCBF = normPath + '/rCBF.nii'
        n1_img = nib.load(rCBF)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        # add padding
        padded = np.pad(img, ((0, 0), (0, 0), (18, 18)), 'constant', constant_values=(0, 0))
        new_img = nib.Nifti1Image(padded, n1_affine, n1_header)
        nib.save(new_img, newrCBF)

        rCBV = path + '/rCBV.nii'
        newrCBV = normPath + '/rCBV.nii'
        n1_img = nib.load(rCBV)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        # add padding
        padded = np.pad(img, ((0, 0), (0, 0), (18, 18)), 'constant', constant_values=(0, 0))
        new_img = nib.Nifti1Image(padded, n1_affine, n1_header)
        nib.save(new_img, newrCBV)

        Tmax = path + '/Tmax.nii'
        newTmax = normPath + '/Tmax.nii'
        n1_img = nib.load(Tmax)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        # add padding
        padded = np.pad(img, ((0, 0), (0, 0), (18, 18)), 'constant', constant_values=(0, 0))
        new_img = nib.Nifti1Image(padded, n1_affine, n1_header)
        nib.save(new_img, newTmax)

        label = path + '/label.nii'
        newLabel = normPath + '/label.nii'
        n1_img = nib.load(label)
        n1_header = n1_img.header
        n1_affine = n1_img.affine
        img = n1_img.get_fdata()
        # add padding
        padded = np.pad(img, ((0, 0), (0, 0), (18, 18)), 'constant', constant_values=(0, 0))
        new_img = nib.Nifti1Image(padded, n1_affine, n1_header)
        nib.save(new_img, newLabel)

getMax()