from core import bot, services, CONFIG
import threading

def setup():
    nodes = services.api.get_dht_nodes()
    tox_bot = bot.ToxBot(bot.ToxOptions(), CONFIG["BOTNAME"], nodes)
    print("ToxBot name: [ %s ]" % CONFIG["BOTNAME"])
    threading.Thread(target=tox_bot.loop).start()

if __name__ == '__main__':
    setup()
