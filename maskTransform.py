
import os
import subprocess
import os
import numpy as np
from glob import glob
import pathlib
import os.path
from os import path


from qtim_tools.qtim_utilities import format_util
from qtim_tools.qtim_utilities import nifti_util

def resample(input_data, output_filename='', input_transform=None, method="slicer", command="Slicer", temp_dir='./',
             interpolation='linear', dimensions=[1, 1, 1], reference_volume=None):
    """ A catch-all function for resampling. Will resample a 3D volume to given dimensions according
        to the method provided.

        TODO: Add resampling for 4D volumes.
        TODO: Add dimension, interpolation, reference parameter. Currently set to linear/isotropic.

        Parameters
        ----------
        input_data: str or array
            Can be a 3D volume or a filename.
        output_filename: str
            Location to save output data to. If left as '', will return numpy array.
        input_transform: str
            detatails TBD, unimplemented
        method: str
            Will perform motion correction according to the provided method.
            Currently available: ['fsl']
        command: str
            The literal command-line string to be inputted via Python's subprocess module.
        temp_dir: str
            If temporary files are created, they will be saved here.

        Returns
        -------
        output: array
            Output data, only if output_filename is left as ''.
    """

    skull_strip_methods = ['slicer']
    if method not in skull_strip_methods:
        print('Input \"method\" parameter is not available. Available methods: ', skull_strip_methods)
        return

    if method == 'slicer':

        # A good reason to have a Class for qtim methods is to cut through all of this extra code.

        temp_input, temp_output = False, False

        if not isinstance(input_data, str):
            input_filename = os.path.join(temp_dir, 'temp.nii.gz')
            nifti_util.save_numpy_2_nifti(input_data, input_filename)
            temp_input = True
        else:
            input_filename = input_data

        if output_filename == '':
            temp_output = True
            output_filename = os.path.join(temp_dir, 'temp_out.nii.gz')

        dimensions = str(dimensions).strip('[]').replace(' ', '')

        if reference_volume or input_transform is not None:
            resample_command = [command, '--launch', 'ResampleScalarVectorDWIVolume', input_filename, output_filename,
                                '-R', reference_volume, '--interpolation', interpolation]
            if input_transform is not None:
                resample_command += ['-f', input_transform]
            print(' '.join(resample_command))
            subprocess.call(resample_command)
        else:
            resample_command = [command, '--launch', 'ResampleScalarVolume', '-i', interpolation, '-s', dimensions,
                                input_filename, output_filename]
            print(' '.join(resample_command))
            subprocess.call(resample_command)

        if temp_input:
            os.remove(input_filename)
            pass

        if temp_output:
            output = format_util.convert_input_2_numpy(output_filename)
            os.remove(output_filename)
            return output

def stuff():
    rawMain = 'F:/Research/data/segmented/'
    f = open('F:/Research/data/errors.txt','a+')
    for x in range(2, 228):
            MRPathFile = rawMain + str(x) + '/' + str(x) + 'label.nii'
            if not os.path.exists(MRPathFile):
                continue
            outpath = rawMain + str(x) + '/MRregistered/'
            if not os.path.exists(outpath):
                os.mkdir(outpath)
            referencePath = outpath + 'registered' + str(x) + '.nii'
            outpathFile = outpath + 'registered' + str(x) + 'label.nii'
            outPathTransform = outpath + 'transform' + str(x) + '.tfm'
            command = 'C:/research/Slicer/Slicer.exe'
            tempdir = rawMain + str(x) + '/'
            resample(MRPathFile, output_filename=outpathFile, input_transform=outPathTransform, method='slicer', command=command, temp_dir=tempdir, interpolation='nn', reference_volume=referencePath)
    return

def resampleVoxel():
    raw = 'F:/Research/data/segmented/'
    resampled = 'F:/Research/data/test/'
    f = open('F:/Research/data/errors.txt','a+')
    for x in range(2, 3):

            label = raw + str(x) + '/MRregistered/registered' + str(x) + 'label.nii'
            #MTT = raw + str(x) + '/MTT.nii'
            #rCBF = raw + str(x) + '/rCBF.nii'
            #rCBV = raw + str(x) + '/rCBV.nii'
            #Tmax = raw + str(x) + '/Tmax.nii'

            if not os.path.exists(label):
                continue

            resampledPath = resampled + str(x) + '/'

            if not os.path.exists(resampledPath):
                os.mkdir(resampledPath)

            outlabel = resampledPath + 'label.nii'
            #outMTT = resampledPath + 'MTT.nii'
            #outrCBF = resampledPath + 'rCBF.nii'
            #outrCBV = resampledPath + 'rCBV.nii'
            #outTmax = resampledPath + 'Tmax.nii'

            command = 'C:/research/Slicer/Slicer.exe'

            resample(label, output_filename=outlabel, method='slicer', command=command, interpolation='nn',
                     dimensions=[1, 1, 1])
            #resample(MTT, output_filename=outMTT, method='slicer', command=command, interpolation='linear',
            #         dimensions=[1, 1, 1])
            #resample(rCBF, output_filename=outrCBF, method='slicer', command=command, interpolation='linear',
            #         dimensions=[1, 1, 1])
            #resample(rCBV, output_filename=outrCBV, method='slicer', command=command, interpolation='linear',
            #         dimensions=[1, 1, 1])
            #resample(Tmax, output_filename=outTmax, method='slicer', command=command, interpolation='linear',
            #         dimensions=[1, 1, 1])

    return

def resampleOvarianVoxel():
    patho = 'C:/Users/Robin/Downloads/raw1'
    baseDir = os.path.normpath(patho)
    files = glob(baseDir + '/*/T1POST/segMask_tumor.nii')
    f = open('F:/Research/data/errors.txt', 'a+')

    for file in files:
        filePath, fileName = os.path.split(file)
        name, ext = fileName.split('.')

        if fileName == 'segMask_tumor.nii':
            newPath = filePath + '\\' + name + '-resampled.nii'
            ref = filePath + '\\' + 'imagingVolume-resampled.nii'
            if not os.path.exists(ref):
                f.write('error ' + ref)
            command = 'C:/research/Slicer/Slicer.exe'
            resample(file, output_filename=newPath, method='slicer', command=command, interpolation='nn', dimensions=[1, 1, 1], reference_volume=ref)
            os.remove(file)

        if fileName == 'imagingVolume.nii':
            newPath = filePath + '\\' + name + '-resampled.nii'
            command = 'C:/research/Slicer/Slicer.exe'
            resample(file, output_filename=newPath, method='slicer', command=command, interpolation='linear', dimensions=[1, 1, 1])
    f.close()
    return

def resampleOvarianVoxelT2():
    patho = 'F:/raw2'
    baseDir = os.path.normpath(patho)
    f = open('F:/Research/data/errors.txt', 'a+')
    files = glob(baseDir + '/*/T2/imagingVolume.nii')

    for file in files:
        filePath, fileName = os.path.split(file)
        name, ext = fileName.split('.')

        if fileName == 'imagingVolume.nii':
            newPath = filePath + '\\' + name + '-resampled.nii'
            command = 'C:/research/Slicer/Slicer.exe'
            resample(file, output_filename=newPath, method='slicer', command=command, interpolation='linear', dimensions=[1, 1, 1])
            os.remove(file)

    files = glob(baseDir + '/*/T2/segMask_tumor.nii')

    for file in files:
        filePath, fileName = os.path.split(file)
        name, ext = fileName.split('.')

        if fileName == 'segMask_tumor.nii':
            newPath = filePath + '\\' + name + '-resampled.nii'
            ref = filePath + '\\' + 'imagingVolume-resampled.nii'
            if not os.path.exists(ref):
                f.write('error ' + ref)
            command = 'C:/research/Slicer/Slicer.exe'
            resample(file, output_filename=newPath, method='slicer', command=command, interpolation='nn', dimensions=[1, 1, 1], reference_volume=ref)
            os.remove(file)

    f.close()
    return

resampleOvarianVoxelT2()

