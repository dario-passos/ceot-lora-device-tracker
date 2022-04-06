from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import LHT65, LSE01, Map, Home

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home|', href='/'),
        dcc.Link('Map|', href='/apps/Map'),
        dcc.Link('Sensores de Copa |', href='/apps/LHT65'),
        dcc.Link('Sensores de Solo', href='/apps/LSE01'),
    ], className="inline-block"),
    html.Div(id='page-content', children=[],)
],  className='container-fluid inline-block',
    style={
        'padding-left':"5%",
        'padding-right':"5%",
    })


# app._favicon = f'{os.getcwd()}\ceot-logo.png'

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return Home.layout
    if pathname == '/apps/Map':
        return Map.layout
    if pathname == '/apps/LHT65':
        return LHT65.layout
    if pathname == '/apps/LSE01':
        return LSE01.layout
    else:
        return Home.layout


if __name__ == '__main__':
    app.run_server(debug=True)