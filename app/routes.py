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


def create_reply(lat, lon):
    data = get_traffic_data(lat, lon)
    road_types = {'FRC0': 'Motorway',
                  'FRC1': 'Major road',
                  'FRC2': 'Other major road',
                  'FRC3': 'Secondary road',
                  'FRC4': 'Local connecting road',
                  'FRC5': 'Local road of high importance',
                  'FRC6': 'Local road'
                  }
    if data['flowSegmentData']['roadCloser']:
        reply = 'Unfortunately this road is closed!'
    else:
        reply = (f"Your nearest road is classified as a _{road_types[data['flowSegmentData']['frc']]}_.  "
                 f"The current average speed is *{data['flowSegmentData']['currentSpeed']} kmph* and "
                 f"would take *{data['flowSegmentData']['currentTravelTime']} seconds* to pass this section of road.  "
                 f"With no traffic, the speed would be *{data['flowSegmentData']['freeFlowSpeed']} kmph* and would "
                 f"take *{data['flowSegmentData']['freeFlowTravelTime']} seconds*.")
    return reply


@app.route('/map')
def create_map():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    data = get_traffic_data(lat, lon)

    points = [(i['latitude'], i['longitude']) for i in data['flowSegmentData']['coordinats']['coordinate']]

    m = folium.Map(location=(lat, lon), zoom_start=15)
    folium.PolyLine(points, color='orange', weight=10).add_to(m)

    return m._repr_html_()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')
