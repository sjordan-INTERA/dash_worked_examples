# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 14:04:29 2025

@author: shjordan
"""

from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import os


# ----------------------
# --- Initialize the app
# ----------------------
app = Dash(__name__)


# --------------------------------------------------
# --- Create a figure from some USGS streamflow data
# --------------------------------------------------
# Load data
data_path = os.path.join('shared_assets','example_river_flow_1.csv')
df = pd.read_csv(data_path,
                 index_col=1,  # We want datetime index, which is the 2nd column (zero-indexed column 1)
                 parse_dates=True) # Auto parse the dates to datetime format

# Filter out bad measurements
df = df.loc[df['flow_cfs'] > 0]

# Create a simple Plotly timeseries figure
fig = px.line(df,
              x=df.index,
              y='flow_cfs'
              )

# Update figure title and x/y axis labels
fig.update_layout(
    yaxis=dict(title='Streamflow (cfs)'),
    xaxis=dict(title='Year'),
    title_text="USGS Streamflow",
    )


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
                      figure=fig)
            ]
        )
    )


# ---------------
# --- Run the app
# ---------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)




