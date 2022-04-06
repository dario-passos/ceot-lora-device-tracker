from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
from app import app
import datetime

from .modules.device import DeviceProfile, Device
from datetime import datetime
from .modules.client import Client
import config as config
import secret
import plotly.graph_objects as go


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys()),
                    list(config.LHT65_FIELDS.keys())[2],
                    id='xaxis-column'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),

        ]),
    dcc.Graph(id='indicator-graphic',
                style={
                  'height':'70vh'
              }),
    ]),
    
    dcc.Checklist(
        id="checklist",
        options=['L'+ str(i) for i in range(1, config.MAX_LHT65_DEVICES + 1)],
        value=['L1'],
        inline=True,
        inputStyle={
            "margin-left": "20px",
            "margin-right": "2px",
        }
    ),
##################################################################################

    html.Hr(),
    html.Div([
            html.Div([
            html.Div([
                dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys()),
                    list(config.LHT65_FIELDS.keys())[0],
                    id='field-7days-lht65'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),

        ]),
        dcc.Graph(  id="graph-mean-last-7-days-lht65",
                    style={
                        'height':'70vh'
                    }),
        dcc.Checklist(
            id="checklist-math",
            options=config.MEASUREMENT_OPTIONS,
            value=['mean'],
            inline=True,
            inputStyle={
                "margin-left": "20px",
                "margin-right": "2px",
            }
        ),
    ]),
##################################################################################

    html.Hr(),
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    config.SIGNAL_FIELDS,
                    config.SIGNAL_FIELDS[0],
                    id='sf-lht65'
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),

        ]),
    ]),
    
    dcc.Graph(id='signal-graphic-lht65',
              style={
                  'height':'70vh'
              }),
    dcc.Checklist(
        id="checklist-signal",
        options=['L'+ str(i) for i in range(1, config.MAX_LHT65_DEVICES + 1)],
        value=['L1'],
        inline=True,
        inputStyle={
            "margin-left": "20px",
            "margin-right": "2px",
        }
    ),

], className='container-fluid inline-block')

##############################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input("checklist", "value"),
    Input('indicator-graphic', 'figure'),)
def update_graph(xaxis_column_name, checklist, graph):

    # vars
    existing_fields = []
    new_data = []

    # new figure
    fig = go.Figure() 
    fig.update_layout(title_text=f'Tree Sensors {xaxis_column_name} measurement', 
                        title_x=0.5,                    
                        xaxis_title='Date',
                        yaxis_title=f'{xaxis_column_name}',)


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
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)

    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    for k in checklist:
        if not k in existing_fields:
            device = Device(k, dp, client, 'Arvores')
            df = device.query_field(xaxis_column_name, START)

            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[xaxis_column_name],
                name=k,
                mode='lines'
               )
            )
    return fig

##################################################################################################################################
@app.callback(
    Output('graph-mean-last-7-days-lht65', 'figure'),
    Input('field-7days-lht65', 'value'),
    Input('checklist-math', 'value'),
    Input('graph-mean-last-7-days-lht65', 'figure'),)
def update_graph_last7days(field, checklist, graph):

    existing_fields = []
    new_data = []

    fig = go.Figure()
    fig.update_layout(title_text=f'Tree Sensors  {field} field last 7 days', 
                    title_x=0.5,                    
                    xaxis_title='Date',
                    yaxis_title=f'{field}')
    if graph != None and graph['layout']['yaxis']['title']['text'] == field:

        # procura os campos existentes
        existing_fields = [g['name'] for g in graph['data']]
        
        # mantem os dados que nao foram removidos da checklist
        new_data = [g for g in graph['data'] if g['name'] in checklist]
        
        # cria grafico sem os dados que foram removidos
        graph['data'] = new_data
        fig = go.Figure(graph)

    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    for k in checklist:
        if not k in existing_fields:
            device = Device('L1', dp, client, 'Arvores')
            df = device.get_mean_days(field,  k, "7",  START)
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[field],
                name=k,))
    return fig



##########################################
@app.callback(
    Output('signal-graphic-lht65', 'figure'),
    Input('sf-lht65', 'value'),
    Input("checklist-signal", "value"),
    Input('signal-graphic-lht65', 'figure'),)
def update_signal_graph(xaxis_column_name, checklist, graph):
    # vars
    existing_fields = []
    new_data = []

    # new figure
    fig = go.Figure() 
    fig.update_layout(title_text=f'Tree Sensors {xaxis_column_name} field', 
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
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    
    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    for k in checklist:
        if not k in existing_fields:
            device = Device(k, dp, client, 'Arvores')
            df = device.query_signal_status(xaxis_column_name, START)
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[xaxis_column_name],
                name=k,
            ))

    return fig

