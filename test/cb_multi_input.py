# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
button1=html.Button("Button1",id='button-1')
button_update_display=html.Div(id='button-update-display')
button_update_display.children='hello everybody'

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    button1,
    html.Button("Button2",id='button-2'),
    button_update_display
])

@app.callback(
    dash.dependencies.Output('button-update-display','children'),
    [dash.dependencies.Input('button-1','n_clicks'),
     dash.dependencies.Input('button-2','n_clicks')])
def do_button_stuff(b1_n_clicks,b2_n_clicks):
    print(b1_n_clicks,b2_n_clicks)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    if changed_id == 'button-1.n_clicks':
        return "budday1: %d" % (b1_n_clicks,)
    elif changed_id == 'button-2.n_clicks':
        button_update_display.children="budday2: %d" % (b2_n_clicks,)
        return dash.no_update 
        #return "budday2: %d" % (b2_n_clicks,)
    else:
        return dash.no_update 

if __name__ == '__main__':
    app.run_server(debug=True)

