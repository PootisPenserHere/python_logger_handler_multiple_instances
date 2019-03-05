import logging
from logging.handlers import RotatingFileHandler


class Example(object):
    def __init__(self):
        self.logger = logging.getLogger("example_logger")
        self.logger.setLevel(logging.INFO)

        self.logger.info("A new instance of the example has been created")


logger = logging.getLogger()
log_handler = RotatingFileHandler('app.log', maxBytes=100 * 1024 * 1024, backupCount=10, mode='a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

for i in iter(range(0, 3)):
    example = Example()