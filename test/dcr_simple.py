# Test dash_cb_router.py

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_cb_router
import pdb

app=dash.Dash(__name__)

app.layout=html.Div(children=[
    html.Button('Increment',id='button-increment'),
    html.Button('Decrement',id='button-decrement'),
    html.Div(id='countdisplay',children='0')
])

cb_router=dash_cb_router.DashCallbackRouter()

def inc_counter(input,states):
    button_increment_nclicks=input
    countdisplay_children=states[0]
    n=int(countdisplay_children)+1
    return [str(n)]

def dec_counter(input,states):
    button_increment_nclicks=input
    countdisplay_children=states[0]
    n=int(countdisplay_children)-1
    return [str(n)]

cb_router.add_cb(
    ['countdisplay.children'],
    'button-increment.n_clicks',
    ['countdisplay.children'],
    inc_counter)

cb_router.add_cb(
    ['countdisplay.children'],
    'button-decrement.n_clicks',
    ['countdisplay.children'],
    dec_counter)

dash_cb_router.register_cbs_with_app(cb_router,app)

if __name__ == '__main__':
    pdb.set_trace()
    app.run_server(port=8051)
