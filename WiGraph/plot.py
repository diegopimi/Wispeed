from flask import Flask
import sched
import time
from datetime import datetime
from file_manager import log_file_path
import plotly.graph_objs as go
import json

scheduler = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)

def graph_download():
    
    with open(log_file_path, 'r') as f:
        data = json.load(f)
    sorted_data = sorted(data, key=lambda x: x['Time'])

    cursor = [{
        'Time': item['Time'],
        'Date': item['Date'],
        'Download': float(item['Download']),  
        'Upload': float(item['Upload'])       
    } for item in sorted_data]
        
    x_values = []
    y_values = []
    for document in cursor:
        date_str = document['Date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        time_str = document['Time']
        datetime_obj = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S')

        x_values.append(datetime_obj)
        y_values.append(document['Download'])

    sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='Download'))  # Add legend for the line

    fig.update_layout(
        title='Download Readings',
        xaxis_title='Date and Time',
        yaxis_title='Download (Mbit/s)',
        legend=dict(title='Legend', orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)  # Adjust legend position
    )
    
    html_output = fig.to_html(full_html=False)
    
    return html_output

def graph_upload():
    with open(log_file_path, 'r') as f:
        data = json.load(f)
   
    sorted_data = sorted(data, key=lambda x: x['Time'])

    cursor = [{
        'Time': item['Time'],
        'Date': item['Date'],
        'Download': float(item['Download']),  
        'Upload': float(item['Upload'])       
    } for item in sorted_data]
        
    x_values = []
    y_values = []
    for document in cursor:
        date_str = document['Date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        time_str = document['Time']
        datetime_obj = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S')

        x_values.append(datetime_obj)
        y_values.append(document['Upload'])

    sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='Upload'))  # Add legend for the line

    fig.update_layout(
        title='Upload Readings',
        xaxis_title='Date and Time',
        yaxis_title='Upload (Mbit/s)',
        legend=dict(title='Legend', orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5)  # Adjust legend position
    )
    
    html_output = fig.to_html(full_html=False)
    
    return html_output