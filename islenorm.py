from __future__ import division
import os
import nibabel as nib
import numpy as np
from glob import glob
from shutil import copyfile

def getMax():
    mainPath = 'F:/Research/isles2'
    mttMax = 0
    rcbfMax = 0
    rcbvMax = 0
    tmaxMax = 0
    labelMax = 0

    baseDir = os.path.normpath(mainPath)
    imagefiles = glob(baseDir + '/*/*.nii')

    f = open('F:/Research/errors.txt', 'a+')

    for file in imagefiles:

        filePath, fileName = os.path.split(file)

        if fileName == 'CT_MTT.nii':
            n1_img = nib.load(file)
            img = n1_img.get_fdata()
            imgmax = img.max()
            if imgmax > mttMax:
                mttMax = imgmax

        if fileName == 'CT_CBV.nii':
            n1_img = nib.load(file)
            img = n1_img.get_fdata()
            imgmax = img.max()
            if imgmax > rcbvMax:
                rcbvMax = imgmax

        if fileName == 'CT_CBF.nii':
            n1_img = nib.load(file)
            img = n1_img.get_fdata()
            imgmax = img.max()
            if imgmax > rcbfMax:
                rcbfMax = imgmax

        if fileName == 'CT_Tmax.nii':
            n1_img = nib.load(file)
            img = n1_img.get_fdata()
            imgmax = img.max()
            if imgmax > tmaxMax:
                tmaxMax = imgmax

        if fileName == 'OT.nii':
            n1_img = nib.load(file)
            img = n1_img.get_fdata()
            imgmax = img.max()
            if imgmax > labelMax:
                labelMax = imgmax

    f.write('MTT: ' + str(mttMax) + '\n')
    f.write('cbf: ' + str(rcbfMax) + '\n')
    f.write('cbv: ' + str(rcbvMax) + '\n')
    f.write('tmax: ' + str(tmaxMax) + '\n')
    f.write('label: ' + str(labelMax) + '\n')
    return

def normalize():
    mainPath = 'F:/Research/isles'
    newPath = 'F:/Research/isles2'

    mttMax = 40.0
    rcbfMax = 10000.0
    rcbvMax = 2000.0
    tmaxMax = 40.0

    baseDir = os.path.normpath(mainPath)
    imagefiles = glob(baseDir + '/*/*.nii')


    for file in imagefiles:

        filePath, fileName = os.path.split(file)
        name, ext = fileName.split('.')
        a = filePath.split('\\')

        startPath = 'F:/Research/isles2'
        nePath = startPath + '/' + a[3]
        newPath = nePath + '/' + fileName

        if not os.path.isdir(startPath):
            os.mkdir(startPath)

        if not os.path.isdir(nePath):
            os.mkdir(nePath)

        if fileName == 'CT_MTT.nii':
            n1_img = nib.load(file)
            n1_header = n1_img.header
            n1_affine = n1_img.affine
            img = n1_img.get_fdata()
            img = np.true_divide(img, mttMax)
            new_img = nib.Nifti1Image(img, n1_affine, n1_header)
            nib.save(new_img, newPath)

        if fileName == 'CT_CBV.nii':
            n1_img = nib.load(file)
            n1_header = n1_img.header
            n1_affine = n1_img.affine
            img = n1_img.get_fdata()
            img = np.true_divide(img, rcbvMax)
            new_img = nib.Nifti1Image(img, n1_affine, n1_header)
            nib.save(new_img, newPath)

        if fileName == 'CT_CBF.nii':
            n1_img = nib.load(file)
            n1_header = n1_img.header
            n1_affine = n1_img.affine
            img = n1_img.get_fdata()
            img = np.true_divide(img, rcbfMax)
            new_img = nib.Nifti1Image(img, n1_affine, n1_header)
            nib.save(new_img, newPath)

        if fileName == 'CT_Tmax.nii':
            n1_img = nib.load(file)
            n1_header = n1_img.header
            n1_affine = n1_img.affine
            img = n1_img.get_fdata()
            img = np.true_divide(img, tmaxMax)
            new_img = nib.Nifti1Image(img, n1_affine, n1_header)
            nib.save(new_img, newPath)

        if fileName == 'OT.nii':
            copyfile(file, newPath)



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