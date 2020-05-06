# Study to see how to serve an image using flask

import flask
import PIL.Image
import plotly
import pdb
from plotly.utils import ImageUriValidator
import io
import base64

server=flask.Flask(__name__)

# pil_image_to_uri seems to encode as png always (currently)
@server.route('/dl_image.png')
def provide_image():
    imgf = PIL.Image.open("assets/Keymaker.jpg")
    uri=ImageUriValidator.pil_image_to_uri(imgf)
    mime,contents=uri.split(';')
    typ,cont=contents.split(',')
    byt=base64.b64decode(cont)
    return flask.send_file(io.BytesIO(byt),mimetype=mime)

