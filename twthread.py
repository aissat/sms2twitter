import threading
from twython import Twython
import settings


class TwitterUpdate(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.twitter = Twython(settings.apikey, settings.apisecret,
                               settings.oauthtoken, settings.oauthsecret)

    def run(self):
        while True:
            message = self.queue.get()
            self.twitter.update_status(status=message)
