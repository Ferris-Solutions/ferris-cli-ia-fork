import logging
from ferris_cli.ferris_cli import FerrisKafkaLoggingHandler
from ferris_cli.ferris_cli import CloudEventsAPI

class Main:
    def __init__(self):
        self.logger = logging.getLogger('kafka_logging')
        kh = FerrisKafkaLoggingHandler("pylog")
        kh.setLevel(logging.INFO)
        self.logger.addHandler(kh)

        
    def run(self):
        while True:
            log = input("> ")
            self.logger.info(log)
if __name__ == "__main__":
    main = Main()
    main.run()