import logging
from logging import StreamHandler

from .config import ApplicationConfigurator, DEFAULT_CONFIG
from .broker import FerrisBroker
from logstash_formatter import LogstashFormatterV1

LOGS_KEY = "ferris_cli.logging"
DEFAULT_TOPIC = 'ferris.logs'


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self, topic=None):
        super().__init__()

        self.topic = topic or ApplicationConfigurator.get(DEFAULT_CONFIG).get('DEFAULT_LOGS_TOPIC', DEFAULT_TOPIC)

    def emit(self, msg):
        msg = self.format(msg)
        FerrisBroker.send(msg, self.topic)


class FerrisLogging(FerrisKafkaLoggingHandler):

    def __init__(self):
        super().__init__()

        self.setFormatter(LogstashFormatterV1())
