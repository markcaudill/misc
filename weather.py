#!/usr/bin/env python3
import argparse
import configparser
import os
import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get weather in the command line.')
    parser.add_argument('--config',
        default=os.path.expanduser('~/.forecast.io'))
    args = parser.parse_args()
    config = configparser.SafeConfigParser()
    config.read([args.config])
    api_key = config.get('Forecast', 'api_key')
    lat, lon = requests.get('http://ip-api.com/csv').text.split(',')[7:9]
    content = requests.get('https://api.forecast.io/forecast/%s/%s,%s' % (
        api_key, lat, lon)).json()

    # Possible `icon`s per https://developer.forecast.io/docs/v2
    emojis = {'clear-day': '☀',
              'clear-night': '🌙',
              'rain': '☔',
              'snow': '🌨',
              'sleet': '⛆',
              'wind': '🍃',
              'fog': '🌁',
              'cloudy': '☁',
              'partly-cloudy-day': '⛅',
              'partly-cloudy-night': '☁'}

    try:
        status = '%s %d°' % (emojis[content['currently']['icon']],
                content['currently']['temperature'])
    except KeyError:
        status = '%d° and %s' % (content['currently']['temperature'],
                content['currently']['summary'])
    print(status)
