from pytox import Tox
from time import sleep, strftime, localtime, time
from math import floor
from services.api import post_data
from core import CONFIG
import os


class ToxOptions(object):
    def __init__(self, ):

        self.ipv6_enabled = True
        self.udp_enabled = True
        self.proxy_type = CONFIG['PROXY_TYPE']  # 1=http, 2=socks
        self.proxy_host = CONFIG['PROXY_HOST']
        self.proxy_port = CONFIG['PROXY_PORT']
        self.start_port = 0
        self.end_port = 0
        self.tcp_port = 0
        self.savedata_type = 0  # 1=toxsave, 2=secretkey
        self.savedata_data = b''
        self.savedata_length = 0
        self.local_discovery_enabled = 0

class ToxBot(Tox):
    def __init__(self, opts, name, nodes):

        if opts is not None:
            super(ToxBot, self).__init__(opts)

        self.self_set_name(name)
        self.save_to_log("Tox ID: %s" % self.self_get_address())

        self.node_idx = 0
        self.nodes = nodes
        self.node = nodes[self.node_idx]
        self.connect(self.node)

    def save_to_log(self, text):
    # data = tox.get_savedata()
        if CONFIG['DEBUG']:
            with open(CONFIG['LOG_FILE'], 'at') as f:
                f.write(text.join('\n\r'))

    def connect(self, node):
        self.save_to_log("Connection  %s:%s:%s" % (node["ipv4"], node["port"] , node["public_key"]))
        self.bootstrap(node["ipv4"], node["port"], node["public_key"])

    def next_node_connection(self):
        nodes_size = len(self.nodes)
        self.node_idx += 1
        if self.node_idx < nodes_size:
            print self.node_idx
            self.node = self.nodes[self.node_idx]
            self.connect(self.node)

    def loop(self):
        is_checked = False
        try:
            self.save_to_log("Start loop handler")
            while True:
                status = self.self_get_connection_status()

                if is_checked and not status:
                    is_checked = False
                    self.next_node_connection()

                if not status and not is_checked and CONFIG['RECONNECT']:
                    is_checked = True

                self.iterate()

                if is_checked and CONFIG['RECONNECT']:
                    sleep(CONFIG['TIMEOUT'])

                sleep(0.03)
        except KeyboardInterrupt:
            print "ToxBot was stopped."

    def on_friend_request(self, pk, message):
        print 'Friend request from %s: %s' % (pk, message)
        self.friend_add_norequest(pk)
        print 'Accepted.'

    def on_friend_message(self, fid, id, msg):
        name = self.friend_get_name(fid)
        self.save_to_log('%s, %s, %s, %s' % (fid, name, id, msg))
        c = post_data({
            'uid': fid,
            'created_at': time(),
            'message': msg
        }, self)
        self.save_to_log("POST Response: %s" % c)
        self.friend_send_message(fid, Tox.MESSAGE_TYPE_NORMAL, c)