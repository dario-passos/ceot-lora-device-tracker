from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px

import pandas as pd
import pathlib
from app import app
import datetime

from .modules.device import DeviceProfile, Device
from datetime import datetime
from .modules.client import Client
import config as config
import secret


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

layout = html.Div([
    html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    list(config.LSE01_FIELDS.keys()),
                    list(config.LSE01_FIELDS.keys())[2],
                    id='xaxis-column-lse01'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),

        ]),
    dcc.Checklist(
        id="checklist-lse01",
        options=['SM'+ str(i) for i in range(1, config.MAX_LSE01_DEVICES + 1)],
        value=['SM1'],
        inline=True,
        inputStyle={
            "margin-left": "20px",
            "margin-right": "2px",
        }
    ),
    dcc.Graph(id='indicator-graphic-lse01'),
    ]),
    html.Hr(),
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    config.SIGNAL_FIELDS,
                    config.SIGNAL_FIELDS[0],
                    id='sf-lse01'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),

        ]),
    ]),
    dcc.Graph(id='signal-graphic-lse01'),
    dcc.Checklist(
        id="checklist-signal-lse01",
        options=['SM'+ str(i) for i in range(1, config.MAX_LSE01_DEVICES + 1)],
        value=['SM1'],
        inline=True,
        inputStyle={
            "margin-left": "20px",
            "margin-right": "2px",
        }
    ),

], className='container-fluid inline-block')



import plotly.graph_objects as go

@app.callback(
    Output('indicator-graphic-lse01', 'figure'),
    Input('xaxis-column-lse01', 'value'),
    Input("checklist-lse01", "value"),
    Input('indicator-graphic-lse01', 'figure'),)
def update_graph(xaxis_column_name, checklist, graph):

    # vars
    existing_fields = []
    new_data = []


    # new figure
    fig = go.Figure() 
    fig.update_layout(title_text=f'Soil sensor {xaxis_column_name} measurement', 
                        title_x=0.5,                    
                        xaxis_title='Date',
                        yaxis_title=f'{xaxis_column_name}')


    # se nao existir grafico ainda e se nao ouver alteração de colunas
    if graph != None and graph['layout']['yaxis']['title']['text'] == xaxis_column_name:

        # procura os campos existentes
        existing_fields = [g['name'] for g in graph['data']]
        
        # mantem os dados que nao foram removidos da checklist
        new_data = [g for g in graph['data'] if g['name'] in checklist]
        
        # cria grafico sem os dados que foram removidos
        graph['data'] = new_data
        fig = go.Figure(graph)


    # inicia o cliente IDB
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LSE01', config.LSE01_FIELDS)
    
    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    for k in checklist:
        if not k in existing_fields:
            device = Device(k, dp, client, 'Solo')
            df = device.query_field(xaxis_column_name, START)
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[xaxis_column_name],
                name=k
            ))
    return fig

################################################################################################################################

@app.callback(
    Output('signal-graphic-lse01', 'figure'),
    Input('sf-lse01', 'value'),
    Input("checklist-signal-lse01", "value"),
    Input('signal-graphic-lse01', 'figure'),)
def update_signal_graph(xaxis_column_name, checklist, graph):
    # vars
    existing_fields = []
    new_data = []

    # new figure
    fig = go.Figure() 
    fig.update_layout(title_text=f'Soil sensor {xaxis_column_name} field', 
                        title_x=0.5,                    
                        xaxis_title='Date',
                        yaxis_title=f'{xaxis_column_name}')


    # se nao existir grafico ainda e se nao ouver alteração de colunas
    if graph != None and graph['layout']['yaxis']['title']['text'] == xaxis_column_name:

        # procura os campos existentes
        existing_fields = [g['name'] for g in graph['data']]
        
        # mantem os dados que nao foram removidos da checklist
        new_data = [g for g in graph['data'] if g['name'] in checklist]
        
        # cria grafico sem os dados que foram removidos
        graph['data'] = new_data
        fig = go.Figure(graph)

    # inicia o cliente IDB
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LSE01', config.LSE01_FIELDS)
    
    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    for k in checklist:
        if not k in existing_fields:
            device = Device(k, dp, client, 'Solo')
            df = device.query_signal_status(xaxis_column_name, START)
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[xaxis_column_name],
                name=k
            ))

    return fig

