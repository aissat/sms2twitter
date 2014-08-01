import time
import threading
from twython import Twython
import settings


class TwitterUpdate(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.twitter = Twython(settings.apikey, settings.apisecret,
                               settings.oauthtoken, settings.oauthsecret)

    def post_message(self, message):
        OK = False
        while not OK:
            try:
                self.twitter.update_status(status=message)
                OK = True
            except:  # FIXME: this is kind of ugly
                print('Could not post message, retry in 2 minutes')
                time.sleep(120)

    def run(self):
        while True:
            message = self.queue.get()
            self.post_message(message)
