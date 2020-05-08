# Test dash_cb_router.py

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_cb_router

app=dash.Dash(__name__)

app.layout=html.Div(children=[
    html.Button('Increment',id='button-increment'),
    html.Button('Decrement',id='button-decrement'),
    html.Div(id='countdisplay',children='0')
])

#cb_router=dash_cb_router.DashCallbackRouter()
#
#def inc_counter(inputs,states,context):
#    button_increment_nclicks=inputs[0]
#    countdisplay_children=inputs[1]
#    n=int(countdisplay_children)+1
#    return [str(n)]
#
#def dec_counter(inputs,states,context):
#    button_increment_nclicks=inputs[0]
#    countdisplay_children=inputs[1]
#    n=int(countdisplay_children)-1
#    return [str(n)]
#
#cb_router.add_cb(
#    ['countdisplay.children'],
#    ['button-increment.nclicks','countdisplay.children'],
#    [],
#    'button_increment.nclicks',
#    inc_counter)
#
#cb_router.add_cb(
#    ['countdisplay.children'],
#    ['button-decrement.nclicks','countdisplay.children'],
#    [],
#    'button_decrement.nclicks',
#    dec_counter)
#
#app.callback=dash_cb_router.register_cbs_with_app(cb_router,app)

#@app.callback(
#    [dash.dependencies.Output('countdisplay','children')],
#    [dash.dependencies.Input('button-increment','n_clicks')],
#    [dash.dependencies.State('countdisplay','children')])
@app.callback(
    [dash.dependencies.Output('countdisplay','children')],
    [dash.dependencies.Input('button-increment','n_clicks'),
     dash.dependencies.Input('countdisplay','children')],
    )
#@app.callback(
#    [dash.dependencies.Output('button-increment','value')],
#    [dash.dependencies.Input('button-increment','n_clicks')])
def inc_counter(button_increment_nclicks,old_child):
    n=int(old_child)
    return (str(n+1),)

if __name__ == '__main__':
    app.run_server(port=8051)
