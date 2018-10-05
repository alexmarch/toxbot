import os
from time import strftime

def get_config():
    return {
        'LOG_FILE': "/data/%s.log" % strftime('%H%m%s%d%m%y'),
        'TIMEOUT': float(os.environ['DTH_HOST_CONNECTION_TIMEOUT']),
        'DEBUG': bool(os.environ['DEBUG']),
        'RECONNECT': False,
        'PROXY_TYPE': int(os.environ['PROXY_TYPE']),
        'PROXY_HOST': os.environ['PROXY_HOST'],
        'PROXY_PORT': int(os.environ['PROXY_PORT']),
        'DHT_NODE_LIST_URL': os.environ['DHT_NODE_LIST_URL'],
        'API_DATA_URL': os.environ['API_DATA_URL']
        }