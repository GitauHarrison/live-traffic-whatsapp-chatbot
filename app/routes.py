from app import app
from flask import render_template, request
from twilio.twiml.messaging_response import MessagingResponse
import folium
import requests


def get_traffic_data(lat, lon):
    params = {'points': f'{lat},{lon}',
              'unit': 'kmph',
              'thickness': 14,
              'key': app.config['TOMTOM_API_KEY']
              },
    base_url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json'
    data = requests.get(base_url, params=params).json()
    return data


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')
