import qtim_tools
import os



mainPath = 'F:/Research/data/raw/'
rawMain = 'F:/Research/data/segmented/'

f = open('F:/Research/data/errors.txt','a+')


for x in range(120, 121):
    try:
        CTpath = mainPath + str(x) + '/CT/rawnii/raw.nii'
        MRPathFile = rawMain + str(x) + '/' + str(x) + '.nii'

        if not os.path.exists(CTpath):
            continue

        if not os.path.exists(MRPathFile):
            continue

        outpath = rawMain + str(x) + '/MRregistered2/'
        if not os.path.exists(outpath):
            os.mkdir(outpath)

        outpathFile = outpath + 'registered' + str(x) + '.nii'

        outPathTransform = outpath + 'transform' + str(x) + '.tfm'

        command = 'C:/research/Slicer/Slicer.exe'

        qtim_tools.qtim_preprocessing.registration.register_volume(MRPathFile, CTpath,output_volume_filename=outpathFile,
                                                                    output_transform_filename=outPathTransform,method='slicer_brainsfit',
                                                                    Slicer_Path= command,
                                                                    transform_type='Rigid,ScaleVersor3D,ScaleSkewVersor3D,Affine',
                                                                    transform_mode='useMomentsAlign',interpolation_mode='Linear',
                                                                    sampling_percentage=0.02)

    except:
        f.write('Error with: ' + str(x))
        continue
