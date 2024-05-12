from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import subprocess
import sched
import time
from datetime import datetime
from functionalities import periodic_reading, returnReading, returnAll, readingAt, scheduler
import plotly.graph_objs as go
import plotly.io as pio

scheduler = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/DBPimi'
mongo = PyMongo(app)

def graph_download():
    # Query MongoDB to get the data, sorted by ascending time values
    cursor = mongo.db.WiSpeed.find({}, {'_id': 0, 'Time': 1, 'Download': 1}).sort('Time', 1)
    
    # Extract x and y values from the query result
    x_values = []
    y_values = []
    for document in cursor:
        # Convert the time string to a datetime object
        time_str = document['Time']
        time_obj = datetime.strptime(time_str, '%H:%M:%S')

        x_values.append(time_obj)
        y_values.append(document['Download'])

    # Sort the x-values (time objects) chronologically
    sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    # Create a Plotly line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='Download'))  # Add legend for the line

    # Update layout to include legend
    fig.update_layout(
        title='Download Readings',
        xaxis_title='Time [HH:MM:SS]',
        yaxis_title='Download (Mbit/s)',
        legend=dict(title='Legend', orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)  # Adjust legend position
    )
    
    # Convert the Plotly figure to HTML
    html_output = fig.to_html(full_html=False)
    
    return html_output

def graph_upload():
    # Query MongoDB to get the data, sorted by ascending time values
    cursor = mongo.db.WiSpeed.find({}, {'_id': 0, 'Time': 1, 'Upload': 1}).sort('Time', 1)
    
    # Extract x and y values from the query result
    x_values = []
    y_values = []
    for document in cursor:
        # Convert the time string to a datetime object
        time_str = document['Time']
        time_obj = datetime.strptime(time_str, '%H:%M:%S')

        x_values.append(time_obj)
        y_values.append(document['Upload'])

    # Sort the x-values (time objects) chronologically
    sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    # Create a Plotly line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='Upload'))  # Add legend for the line

    # Update layout to include legend
    fig.update_layout(
        title='Download Readings',
        xaxis_title='Time [HH:MM:SS]',
        yaxis_title='Download (Mbit/s)',
        legend=dict(title='Legend', orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)  # Adjust legend position
    )
    
    # Convert the Plotly figure to HTML
    html_output = fig.to_html(full_html=False)
    
    return html_output