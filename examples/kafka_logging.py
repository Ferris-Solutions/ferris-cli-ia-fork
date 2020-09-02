import logging
from ferris_cli.ferris_cli import FerrisKafkaLoggingHandler
from ferris_cli.ferris_cli import CloudEventsAPI
from logstash_formatter import LogstashFormatterV1
import os



logger = logging.getLogger(os.environ['APP_NAME'])
kh = FerrisKafkaLoggingHandler()
kh.setLevel(logging.INFO)
formatter = LogstashFormatterV1()
kh.setFormatter(formatter)
logger.addHandler(kh) 

logger.info('loading file') 
print('sent logs')
