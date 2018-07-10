import nibabel as nib
import numpy as np
from tvtk.api import tvtk,write_data
import vtk
from vtk.util import numpy_support

nii=nib.load('Annotation2014.nii.gz')

reader=tvtk.NIFTIImageReader()
reader.file_name='Annotation2014.nii.gz'
reader.update()

image=reader.get_output()
image.origin=nii.affine[0:3,3]
vImage=tvtk.to_vtk(image)
vPD=vImage.GetPointData()
vSC=vPD.GetScalars()
data=numpy_support.vtk_to_numpy(vSC)

indxs=np.unique(data)

for ind in indxs[1:]:
  print ind
  tmp=data.copy()
  tmp[tmp!=ind]=0
  tmp[tmp==ind]=1
  
  vPD.SetScalars(numpy_support.numpy_to_vtk(tmp))
  image=tvtk.to_tvtk(vImage)
  
  iso=tvtk.MarchingCubes()
  iso.set_input_data(image)
  iso.set_value(0,0.5)
  iso.update()
  smoother = tvtk.SmoothPolyDataFilter()
  smoother.convergence=0
  smoother.number_of_iterations=30
  smoother.relaxation_factor=0.1
  smoother.feature_angle=60
  smoother.feature_edge_smoothing=True
  smoother.boundary_smoothing=True
  smoother.set_input_data_object(iso.get_output_data_object(0))
  smoother.update()

  write_data(smoother.get_output_data_object(0) ,'out_'+str(ind)+'.vtk')
