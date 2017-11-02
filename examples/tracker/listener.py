import logging
import tornado.web

from .models import ClientManager
from open_blockchain.network import get_client_id

logger = logging.getLogger()


class Listener(tornado.web.RequestHandler):

    def process_request(self):
        try:
            cm = ClientManager()
            cm.update(get_client_id(self.request))
            return cm.get()
        except Exception as e:
            logger.error(e)

    def get(self):
        logger.info('Processing get request')
        data = self.process_request()

        self.set_header('Content-Type', 'application/json')
        self.write(data.__bytes__())
        self.finish()