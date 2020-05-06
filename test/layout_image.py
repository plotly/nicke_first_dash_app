import plotly.graph_objects as go
import PIL.Image
import sys
import numpy as np
import skimage.util

# convert from numpy array to PIL.Image to show that this is possible
imgf = PIL.Image.open("assets/Keymaker.jpg")
img_arrayf=skimage.util.img_as_float(np.array(imgf))
img_array=skimage.util.img_as_ubyte(img_arrayf)
print(img_array.dtype)
img=PIL.Image.fromarray(img_array)
width, height = img.size

fig=go.Figure(go.Scatter(x=[],y=[]))
fig.add_layout_image(dict(source=img,
                          xref="x",
                          yref="y",
                          x=0,
                          y=0,
                          sizex=width,
                          sizey=height,
                          sizing="contain",
                          layer="below"))
fig.update_layout(template=None)
fig.update_xaxes(showgrid=False, range=(0, width))
fig.update_yaxes(showgrid=False, scaleanchor='x', range=(height, 0))

with open('/tmp/website.html','w') as fd:
    fd.write(fig.to_html(include_plotlyjs='cdn'))
