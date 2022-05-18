from math import prod
from time import sleep
from click import option
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from machine_simulation import Machine
import dash_cytoscape as cyto
import networkx as nx
from collections import deque


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

mach = Machine(normal_capacity=100, cap_uncertainty=5, outage_prob=0.04, exp_outage_length=3)


dropdown_data = ["MACHINE" + str(i) for i in range(1, 5)]

app.layout = dbc.Container([

    html.H1("Manufacturing Dashboard with Python Dash", style={"text-align": "center"}),

    dcc.Dropdown(id="select_branch",
                 options=[{"label": i, "value":i} for i in dropdown_data],
                 multi=False,
                 value = "MACHINE1",
                 style={"width":"40%"}),

    dcc.Graph(id="live-graph", animate=True,
              style={"width":"40%"}),
                 
    html.Div(id="staus_container", children=[]),

    dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals = 0
        ),
])

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(100)

# @app.callback(
#     [Output(component_id="output_container", component_property="children"),
#      Output(component_id="status_container", component_property="children"),
#      Output(component_id="production_history", component_property="figure")],
#     [Input(component_id="select_branch", component_property="value")]
# )

@app.callback([Output('live-graph', "figure"), Output("staus_container", "children")], 
              [Input('graph-update', 'n_intervals')])

        
def update_graph(option_selected):
    X.append(X[-1]+1)
    production = mach.simulate(1)[0] # mach.simulate(1)
    Y.append(production)
    
    if X[-1] == 0:
        status = "Offline"
    else:
        status = "Online"

    production_history_fig = px.line(y=list(Y), x=list(X), title="Production")
    production_history_fig.update_xaxes(range=[min(X),max(X)])
    production_history_fig.update_yaxes(range=[0,max(Y)])


    return production_history_fig, status


if __name__ == "__main__":
    app.run_server(debug=True)