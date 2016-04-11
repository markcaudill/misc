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
    print('%d° and %s' % (content['currently']['temperature'],
                          content['currently']['summary']))
