import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import dash_cytoscape as cyto
import networkx as nx
import plotly.graph_objects as go
from datetime import datetime

now = datetime.now()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# prepare the data
df = pd.read_csv("Production-Systems\\Data\\Wafer_TEST.tsv", delimiter="\t", header=None)
df.drop(columns=0, inplace=True)
dropdown_data = ["Sensor: "+ str(i) for i in df.index]

fig = go.Figure()
fig.add_trace(go.Scatter(y=df.loc[0], name="Sensor 0"))
fig.add_trace(go.Scatter(y=df.loc[1], name="Sensor 1"))
fig.update_layout(
    title="",
    xaxis_title="Time",
    yaxis_title="Value",
)

corr = np.round(np.corrcoef(df.loc[0],df.loc[1])[0][1], 2)

print(corr)


diff_fig = px.area(df.loc[0] - df.loc[1])

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.Div("Location: Dresden")),
        dbc.Col(html.Div("Number of Sensors connected: {}".format(len(df)))),
    ]),

    html.H1("Wafer production Monitoring", style={"text-align": "center"}),

    dcc.Dropdown(id="add-sensor",
                 options=[{"label": i, "value":i} for i in dropdown_data],
                 style={"width":"40%"},
                 multi=True,
                 placeholder="Select a Sensor",
                 value=["Sensor: 0"]),

    html.Div(id="comparson-stats", children=[f"The correlation is: {corr}"]),

    dcc.Graph(id="live-graph", animate=True,
              style={"width":"90%"}, figure=fig),

    dcc.Graph(id="difference-graph", animate=True,
              style={"width":"90%"}, figure=diff_fig),
                 
    html.Div(id="staus_container", children=["Sensor data is fetched every 1000 miliseonds (i.e. every second)"]),
    html.Div(children=["Sensor data is fetched every 1000 miliseonds (i.e. every second)"]),
    html.Div(children=["Link to Dataset: http://www.timeseriesclassification.com/description.php?Dataset=Wafer"]),
    html.Div(children=["The dataset is part of a PhD thesis by Robert Olszewski on Time Series Classification, Link to thesis: https://dl.acm.org/citation.cfm?id=935627"]),

    dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals = 0,
            disabled=False
        ),

    dcc.RadioItems(id="process-status", options=['Run fetching process  ', 'Stop fetching'], value='Run fetching process')

])


@app.callback([Output("staus_container", "children")], 
              [Input('graph-update', 'n_intervals')])

def update_figure(inp):
    time = datetime.now()
    return ["Current Time: {}".format(time)]


@app.callback([Output("graph-update", "disabled")], 
              [Input("process-status", "value")])

def stop_fetch(x):
    if x == "Run fetching process  ":
        return [False]
    else:
        return [True]


#@app.callback([Output("live-graph", "figure")],
#              [Input("add-sensor", "value")])
#def updata_graph(selected):
#    print(selected)
#    print("lel")
#    fig = go.Figure()
#    # fig.add_trace(go.Scatter(y=df.loc[0], name="Sensor 0"))
#    # fig.add_trace(go.Scatter(y=df.loc[1], name="Sensor 1"))
#    fig.update_layout(
    #    title="lelel",
#    xaxis_title="Time",
#    yaxis_title="Value",
#    )
#    if selected:
#        for i in selected:
#            fig.add_trace(go.Scatter(y=df.loc[int(i.split()[1])], name=i))
#    
#    return [fig]


if __name__ == "__main__":
    app.run_server(debug=True)