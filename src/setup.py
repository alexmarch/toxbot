from core import bot, utils
import threading

def setup():
    nodes = utils.get_dht_nodes()
    tox_bot = bot.ToxBot(bot.ToxOptions(), "TestToxBot", nodes)
    print("ToxBot starting...")
    threading.Thread(target=tox_bot.loop).start()

if __name__ == '__main__':
    setup()


