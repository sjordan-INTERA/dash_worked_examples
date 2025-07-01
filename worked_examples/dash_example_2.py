# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 14:04:29 2025

@author: shjordan
"""

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import os


# ----------------------
# --- Initialize the app
# ----------------------
app = Dash(__name__)


# --------------------------------------------------
# --- Create a figure from some USGS streamflow data
# --------------------------------------------------
def make_figure(log_scale=False,
                red_line=False,
                dataset='Streamflow 1'):
    # Load data
    ts = dataset.split()[-1]  # --> This will return either 1 or 2, and load the corresponding dataset
    data_path = os.path.join('shared_assets',f'example_river_flow_{ts}.csv')
    df = pd.read_csv(data_path,
                     index_col=1,  # We want datetime index, which is the 2nd column (zero-indexed column 1)
                     parse_dates=True) # Auto parse the dates to datetime format
    df.columns = ['streamflow_cfs']
    # Filter out bad measurements
    df = df.loc[df['streamflow_cfs'] > 0]
    
    # Create a Plotly timeseries figure using graph_objects
    # 1. Initialize the figure object
    fig = go.Figure()
    # 2. Add a trace (any kind of plot) to the figure, in this case, a scatter plot
    fig.add_trace(
        go.Scatter(x=df.index,
                   y=df['streamflow_cfs'],
                   # By default, go.Scatter is actually a line plot
                   # Using line=dict(...) and marker=dict(...) you can edit appearance of lines and markers
                   line=dict(color='red' if red_line else 'blue')
                   )
        )
    
    # Update figure title and x/y axis labels and log scale option
    fig.update_layout(
        yaxis=dict(title='Streamflow (cfs)',type='log' if log_scale else 'linear'),
        xaxis=dict(title='Year'),
        title_text="USGS Streamflow",
        )
    return fig

fig = make_figure()


# -------------------------------
# --- Create a simple html layout
# -------------------------------
app.layout = (
    # Div acts as a container, can put anything inside of it
    html.Div(
        # The 'children' componet of a Div is what's placed inside of it
        children=[
            
            # dcc.Graph is the object that is able to display Plotly figures
            dcc.Graph(id='display_graph',
                      figure=fig),
            html.Hr(),
            
            # Add a dropdown menu to select a different stream gage to plot
            dcc.Dropdown(['Streamflow 1','Streamflow 2'],
                         style=dict(width="40%"),
                         id='data_selector_dd'),
            html.Hr(),
            
            # Add a checklist of plot options
            html.H4('Plot Options:'),
            dcc.Checklist(['Log Scale','Plot data in red'],
                          id='options_checklist'),
            ]
        )
    )


# -----------------------------
# --- Callback for plot options
# -----------------------------
@app.callback(
    Output('display_graph','figure'),
    Input('options_checklist','value'),
    Input('data_selector_dd','value'),
    prevent_initial_call=True
    )
def update_to_log_scale(value,dataset):
    # Handle case where no options are selected (i.e. value will be None)
    if value:
        log_scale = True if 'Log Scale' in value else False
        red = True if 'Plot data in red' in value else False
    else:
        log_scale = False
        red = False
    
    fig = make_figure(log_scale=log_scale,
                      red_line=red,
                      dataset=dataset)
    
    return fig
        

# ---------------
# --- Run the app
# ---------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)




