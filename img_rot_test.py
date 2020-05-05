import numpy as np
import img_transform
import plot_common
import skimage.io
import skimage.transform
import plotly.graph_objects as go

x=plot_common.path_to_img_ndarray('assets/Keymaker.jpg')
#x=x[:10,:10,:]
xrot=skimage.transform.rotate(x,90)
print('x',x.shape)
print('xrot',xrot.shape)
print(np.sum(xrot!=0))
print(xrot.max())
print(xrot.min())
#fig=go.Figure(data=go.Image(z=xrot))
#x=np.transpose(x,(1,0,2))
img_trace=go.Image(z=xrot,zmax=[1,1,1,1])
fig=go.Figure(data=img_trace)
fig.show()
