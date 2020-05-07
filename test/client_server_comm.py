__doc__="""
Investigation into the mechanics of dealing with data in the browser and on the
server.

Client can select image from their disk.
Server gets the image data and stores it in a dictionary in memory.
Client can manipulate the image, and this manipulated data is sent back to browser.
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import time
import plot_common
import plotly.graph_objects as go
from skimage.color import rgb2gray
from skimage import transform
import pdb
import numpy as np
import flask
from plotly.utils import ImageUriValidator
import io
import os
import uuid

server=flask.Flask(__name__)

app=dash.Dash(server=server)

app.layout=html.Div(children=[
    dcc.Store(id='img_array'),
    dcc.Upload(
        id='uploader',
        children=html.Button('Load Image'),
        multiple=False),
    html.Button(
        'Rotate Clockwise',
        id='rotate_cw'),
    html.Button(
        'Rotate Counter-clockwise',
        id='rotate_ccw'),
    html.Div(id='dummy'),
    dcc.Graph(id='graph',figure=plot_common.dummy_fig()),
    html.Div(id='button1_n_clicks_display'),
    html.A(id='download',children='Download image',href='/0000.png')
    ])

@app.callback(
    [dash.dependencies.Output('download','href')],
    [dash.dependencies.Input('download','n_clicks')])
def update_image_num(download_n_clicks):
    """
    This is used simply to update the href so that browsers don't just use a
    cached image.
    """
    return ("/%s.png" % (uuid.uuid4().hex,),)

img_array = [None]

@app.callback(
    [dash.dependencies.Output('graph','figure')],
    [dash.dependencies.Input('uploader','contents'),
        dash.dependencies.Input('rotate_cw','n_clicks'),
        dash.dependencies.Input('rotate_ccw','n_clicks')])
def my_callback(uploader_contents,
                rotate_cw_n_clicks,
                rotate_ccw_n_clicks):
    print('my_callback: procid: %d, img_array id: %#x' % (os.getpid(),id(img_array),))
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if changed_id == 'uploader.contents':
        if (uploader_contents is not None) and (len(uploader_contents) > 0):
            # just take first image for now
            c=uploader_contents
            t,s=c.split(',')
            img_array[0]=plot_common.base64_to_img_array(s)
    elif changed_id == 'rotate_cw.n_clicks' and img_array[0] is not None:
        img_array[0]=transform.rotate(
            img_array[0],-90,resize=True)
    elif changed_id == 'rotate_ccw.n_clicks' and img_array[0] is not None:
        img_array[0]=transform.rotate(
            img_array[0],90,resize=True)
    if img_array[0] is not None:
        return (plot_common.img_array_to_layout_image_fig(img_array[0]),)
    else:
        return (dash.no_update,)

# pil_image_to_uri seems to encode as png always (currently)
@server.route('/<somehash>.png')
def provide_image(somehash):
    # Just ignore somehash and provide the image in memory, this is just to
    # avoid caching by browsers
    print('provide_image: procid: %d, img_array id: %#x' % (os.getpid(),id(img_array),))
    if img_array[0] is not None:
        mime,byt=plot_common.img_array_to_mime_bytes(img_array[0])
        return flask.send_file(io.BytesIO(byt),mimetype=mime)
    else:
        return "<b>No image to download!</b>"

if __name__ == '__main__':
    app.run_server(port=8051)
