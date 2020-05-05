import base64
import PIL.Image
import io
import numpy as np
import pdb
import plotly.graph_objects as go
import skimage.util

def path_to_img_ndarray(path):
    with open(path,'rb') as fp:
        img=PIL.Image.open(fp)
        img_array=np.array(img)
        return skimage.util.img_as_float(img_array)

def str_to_img_ndarrary(s):
    """
    Returns image in ndarray.
    ndarray will have dimensions (width,height,number_of_color_channels)
    This format is compatible with skimage
    """
    img=PIL.Image.open(io.BytesIO(s))
    img_array=np.array(img)
    return skimage.util.img_as_float(img_array)

def base64_to_img_array(data):
    decoded_img=base64.b64decode(data)
    return str_to_img_ndarrary(decoded_img)

def str_to_img_trace(s):
    img_array=str_to_img_ndarrary(s)
    img_trace=go.Image(z=img_array)
    return img_trace

def base64_to_img_trace(data):
    decoded_img=base64.b64decode(data)
    return str_to_img_trace(decoded_img)
