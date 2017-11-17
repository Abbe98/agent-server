import requests
import user_agents
from flask import Flask
from flask import request
from flask import jsonify

freegeoip_endpoint = 'https://freegeoip.net/'
cors_value = '*'

app = Flask(__name__)

def ua_string_to_dict(ua_string):

    ua_object = {}
    ua_object['browser'] = {}
    ua_object['os'] = {}
    ua_object['device'] = {}

    if not ua_string:
        ua_object['browser']['name'] = None
        ua_object['browser']['version'] = None

        ua_object['os']['name'] = None
        ua_object['os']['version'] = None

        ua_object['device']['name'] = None
        ua_object['device']['brand'] = None
        ua_object['device']['model'] = None
        ua_object['device']['type'] = None
        ua_object['device']['touch_capable'] = None

        return ua_object

    ua = user_agents.parse(ua_string)
    ua_object['browser']['name'] = ua.browser.family
    ua_object['browser']['version'] = ua.browser.version[0]

    ua_object['os']['name'] = ua.os.family
    ua_object['os']['version'] = ua.os.version_string

    ua_object['device']['name'] = ua.device.family
    ua_object['device']['brand'] = ua.device.brand
    ua_object['device']['model'] = ua.device.model
    ua_object['device']['type'] = get_device_type(ua)
    ua_object['device']['touch_capable'] = ua.is_touch_capable

    return ua_object

def get_device_type(ua):
    if ua.is_mobile:
        return 'Mobile'
    elif ua.is_pc:
        return 'Desktop'
    elif ua.is_bot:
        return 'Bot'
    elif ua.is_tablet:
        return 'Tablet'

    return 'Unknown'

def get_data_from_ip(ip):
    r = requests.get(freegeoip_endpoint + 'json/' + ip)

    geo = {}

    if not r.status_code == 200:
        geo['ip'] = None
        geo['country_code'] = None
        geo['country'] = None
        geo['region'] = None
        geo['city'] = None
        geo['time_zone'] = None
        geo['latitude'] = None
        geo['longitude'] = None

        return geo

    data = r.json()
    geo['ip'] = data['ip']
    geo['country_code'] = data['country_code']
    geo['country'] = data['country_name']
    geo['region'] = data['region_name']
    geo['city'] = data['city']
    geo['time_zone'] = data['time_zone']
    geo['latitude'] = data['latitude']
    geo['longitude'] = data['longitude']

    return geo

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = cors_value
    return response

@app.route('/')
def agent():
    data = ua_string_to_dict(request.headers.get('User-Agent'))
    data['geo'] = get_data_from_ip(request.environ['REMOTE_ADDR'])
    return jsonify(data)

if __name__ == '__main__':
    app.run()
