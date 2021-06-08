import logging
from logging import StreamHandler

from .config import ApplicationConfigurator, DEFAULT_CONFIG
from .broker import FerrisBroker

LOGS_KEY = "ferris_cli.logging"
DEFAULT_TOPIC = 'ferris.logs'


class FerrisLogging:

    def log(self, record, topic=None):
        return FerrisKafkaLoggingHandler().log(record, topic)


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self):
        super().__init__()

    def log(self, record, topic=None):

        if not topic:
            topic = ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_LOGS_TOPIC', DEFAULT_TOPIC)

        try:
            msg = self.format(record)
            resp = FerrisBroker.send(msg, topic)

            logging.getLogger(LOGS_KEY).info("Response from broker.send: %s ", str(resp))
        except Exception as e:
            logging.getLogger(LOGS_KEY).error("Error while sending logs:")
            logging.getLogger(LOGS_KEY).exception(e)

        return True

