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
import skimage.transform
import pdb
import numpy as np

app=dash.Dash(__name__)

app.layout=html.Div(children=[
    dcc.Store(id='img_array'),
    dcc.Upload(
        id='uploader',
        children=html.Div([
            html.A('Select Files')
        ]),
        multiple=True),
    html.Button(
        'Rotate Clockwise',
        id='rotate_cw'),
    html.Button(
        'Rotate Counter-clockwise',
        id='rotate_ccw'),
    html.Div(id='dummy'),
    dcc.Graph(id='graph'),
    html.Div(id='button1_n_clicks_display')
    ])

img_array=np.array([])

class image_mod_cb:
    """ This is a little funny because it's static. """
    @app.callback(
        [dash.dependencies.Output('graph','figure')],
        [dash.dependencies.Input('uploader','contents'),
         dash.dependencies.Input('rotate_cw','n_clicks'),
         dash.dependencies.Input('rotate_ccw','n_clicks')])
    def __call__(uploader_contents,
                 rotate_cw_n_clicks,
                 rotate_ccw_n_clicks):
        try:
            img_array=img_array
        except NameError:
            img_array=None
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if changed_id == 'uploader.contents':
            if (uploader_contents is not None) and (len(uploader_contents) > 0):
                # just take first image for now
                c=uploader_contents[0]
                t,s=c.split(',')
                img_array=plot_common.base64_to_img_array(s)
        elif changed_id == 'rotate_cw.n_clicks':
            img_array=skimage.transform.rotate(
                img_array,-90,resize=True)
        elif changed_id == 'rotate_ccw.n_clicks':
            img_array=skimage.transform.rotate(
                img_array,90,resize=True)
        if img_array is not None:
            img_trace=go.Image(z=img_array,zmax=[1,1,1,1])
            return (go.Figure(data=img_trace),)
        return dash.no_update
    
if __name__ == '__main__':
    app.run_server(debug=True,threaded=False)
