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
import plotly.graph_objects as go

import pandas as pd


lht65_location = pd.read_csv("lht65_device_loc.csv")


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())
layout = html.Div([
      dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys()),
                    list(config.LHT65_FIELDS.keys())[2],
                    id='mapbox-fields'
                ),
        dcc.Graph(id='mapbox1', style={
            'width':'90vw',
            'height':'100vh'
        }),
]),

@app.callback(
    Output('mapbox1', 'figure'),
    Input('mapbox-fields', 'value'))
def mapbox(field):

     
    ## Color scales: 
    #        bat -> 'RdYlGn'
    #        tmp ->'Portland'
    #        ilx -> 'blackbody'
    #        hum -> 'YlGnBu'
    
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    
    tmp = []
    for index, row in lht65_location.iterrows():
        device = Device(row['Device'], dp, client, 'Arvores')
        df,time = device.get_last_value(field)
        tmp.append(df)
        
    clone = lht65_location.__deepcopy__()

    clone[field] = tmp
    field_label = str(field)
    field_color = {'bat':'RdYlGn', 'tmp':'Portland', 
                   'ilx':'blackbody', 'hum':'YlGnBu'}

    
    ## Option 1 -> Scatter plot
    # fig = px.scatter_mapbox(clone, lat='Lat', lon='Lon', color=tmp, size=tmp,
    #                     center=dict(lat=37.192723, lon=-8.182952), zoom=18,
    #                     mapbox_style="stamen-terrain", 
    #                     color_continuous_scale = field_color[field],
    #                     labels = {'color': field_label, 'size':''},
    #                     color_continuous_midpoint = (max(tmp)-min(tmp))/2.,
    #                     range_color=[min(tmp), max(tmp)],
    #                     opacity=0.75,
    #                     )
    ## Option 2 -> Density plot 
    # fig = px.density_mapbox(clone, lat='Lat', lon='Lon', z=tmp, radius=75,
    #                     center=dict(lat=37.192723, lon=-8.182952), zoom=18,
    #                     mapbox_style="stamen-terrain", 
    #                     color_continuous_scale = field_color[field],
    #                     labels = {'z': field_label},
    #                     color_continuous_midpoint = (max(tmp)-min(tmp))/2.,
    #                     range_color=[min(tmp), max(tmp)],
    #                     opacity=0.75,
    #                     )
    fig = px.scatter_mapbox(clone, lat='Lat', lon='Lon', color=tmp, size=tmp,
                        center=dict(lat=37.192723, lon=-8.182952), zoom=18,
                        mapbox_style="stamen-terrain", 
                        color_continuous_scale = field_color[field],
                        labels = {'color': field_label, 'size':''},
                        color_continuous_midpoint = (max(tmp)-min(tmp))/2.,
                        range_color=[min(tmp), max(tmp)],
                        opacity=0.75,
                        )
    # Option 3 -> Hexagonal mesh plot
    # fig = ff.create_hexbin_mapbox(data_frame=clone, lat='Lat', lon='Lon', 
    #                               nx_hexagon=5,
    #                               center=dict(lat=37.192723, lon=-8.182952), zoom=18,
    #                               color = tmp,
    #                               labels = {'color': field_label},
    #                               mapbox_style="stamen-terrain", 
    #                               range_color=[min(tmp), max(tmp)],
    #                               show_original_data=True,
    #                               opacity=0.5, min_count=1
    #                     )
    fig.update_layout(
        mapbox_accesstoken=secret.MAPBOX_TOKEN, 
        # mapbox_bearing = -21,
        mapbox_style='satellite-streets',
        mapbox=dict(
            center=dict(
                lat=37.192723,
                lon=-8.182952
            )),)
    fig.update_geos(projection_type="orthographic" )

    return fig