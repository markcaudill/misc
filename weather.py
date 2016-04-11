#!/usr/bin/env python3
import argparse
import configparser
import os
import requests
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get weather in the command line.')
    parser.add_argument('--config',
        default=os.path.expanduser('~/.forecast.io'))
    parser.add_argument('--no-emoji', default=False,
        action='store_true')
    args = parser.parse_args()
    config = configparser.SafeConfigParser()
    config.read([args.config])
    try:
        api_key = config.get('Forecast', 'api_key')
    except configparser.NoSectionError:
        print('Unable to find a "Forecast" section in %s.' % args.config)
        sys.exit(1)
    except configparser.NoOptionError:
        print('Unable to find "api_key" in the "Forecast" section in %s.' %
                args.config)
        sys.exit(1)
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

    if args.no_emoji is True:
        status = '%d° %s now; %d° %s today; %d° %s tomorrow' % (
                content['currently']['temperature'],
                content['currently']['summary'],
                content['daily']['data'][0]['temperatureMax'],
                content['daily']['data'][0]['summary'][:-1],
                content['daily']['data'][1]['temperatureMax'],
                content['daily']['data'][1]['summary'][:-1])
    else:
        status = '%s %d° now; %s %d° today; %s %d° tomorrow' % (
                emojis[content['currently']['icon']],
                content['currently']['temperature'],
                emojis[content['daily']['data'][0]['icon']],
                content['daily']['data'][0]['temperatureMax'],
                emojis[content['daily']['data'][1]['icon']],
                content['daily']['data'][1]['temperatureMax'])
    print(status)
