import os
from glob import glob

path = 'C:/Users/Robin/Downloads/raw1'
baseDir = os.path.normpath(path)
filesa = glob(baseDir+'/*/T1POST/imagingVolume.nii')
#dcmfilesa = glob(baseDir+'/*/T1POST/segMask_tumor.nii')

#filesb = glob(baseDir+'/*/T2/imagingVolume.nii')
#dcmfilesb = glob(baseDir+'/*/T2/segMask_tumor.nii')


for file in filesa:
    os.remove(file)
#for file in dcmfilesa:
#    os.remove(file)

#for file in filesb:
#    os.remove(file)
#for file in dcmfilesb:
#    os.remove(file)