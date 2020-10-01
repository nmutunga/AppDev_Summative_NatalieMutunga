import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from Predictions import final_dataframe
import flask
from flask import Flask
import plotly.graph_objs as go



def MyDashApp(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    d_app = dash.Dash(__name__,
                    server=server,
                    routes_pathname_prefix='/dashapp/',
                    external_stylesheets=external_stylesheets
                    )

    base_styles = {
        "text-align": "center",
        "border": "1px solid #ddd",
        "padding": "7px",
        "border-radius": "2px",
    }

    Solar_output = final_dataframe['Corrected_SolarFarm_Output']
    Wind_output = final_dataframe['Corrected_WindFarm_Output']
    Total_Output = final_dataframe['Total_Output(MW)']
    metric = final_dataframe['date']

    trace1 = go.Bar(x=metric, y=Solar_output, name='Solar_Output(MW)')
    trace2 = go.Bar(x=metric, y=Wind_output, name='Wind_Output(MW)')
    trace3 = go.Bar(x=metric, y=Total_Output, name='Total_Output(MW)')

    data = [trace1, trace2]
    layout = go.Layout(barmode='group', xaxis_title='Date', yaxis_title='Power Generated')
    fig = go.Figure(data=data, layout=layout)

    d_app.layout = html.Div([
            html.H1(
                children='Dashboard',
                style={
                    'textAlign': 'center',
                }
            ),
            html.Div(
                children='Predicted Power Output for a Wind farm in Klushof, Germany and a Solar Plant in Malpas-Trenton, Australia',
                style={
                    'textAlign': 'center',
                }),
            dcc.Graph(
                id='Graph1',
                figure=fig
            ),
            dcc.Graph(
                id='Graph2',
                figure=go.Figure(data=[trace3], layout=go.Layout(xaxis_title='Date', yaxis_title='Total_Output(MW)'))
            ),
            dcc.Upload
            (html.Button('Upload CSV', id='upload_csv',
                         style={'display':'black', 'padding':"7px"})),

    ])
    #init_callback(d_app)
    return d_app.server

# def init_callback(d_app):
#     @d_app.callback(
#         dash.dependencies.Output('button-basic', 'children'),
#         [dash.dependencies.Input('submit-val', 'n_clicks')],
#     )

    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )