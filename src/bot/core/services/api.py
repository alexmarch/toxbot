import json, urllib2, urllib
from core import CONFIG

# Get list of nodes from WIKI API
def get_dht_nodes():
    f = urllib2.urlopen(CONFIG['DHT_NODE_LIST_URL'])
    j_resp = json.loads(f.read())
    return j_resp["nodes"]

def post_data(data, bot):
    req = urllib2.Request(CONFIG['API_ADMIN_ENDPOINT'], urllib.urlencode(data), {'Content-type':'application/json'})
    try:
        content = urllib2.urlopen(req).read()
        return content
    except urllib2.URLError:
        bot.save_to_log("Wrong post data url %s" % CONFIG['API_ADMIN_ENDPOINT'])
    return None
