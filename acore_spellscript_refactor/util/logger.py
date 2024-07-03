import logging


class Logger():
    _logger = None
    def __init__(self, level=logging.INFO):
        logger = logging.getLogger(__name__)
        logger.setLevel(level)

        # Create a formatter to define the log format
        format = "%(levelname)s:%(filename)s:%(lineno)03d:%(funcName)20s():%(message)s"
        # format = "%(levelname)s:%(filename)s:%(funcName)s():%(message)s"
        formatter = logging.Formatter(format)

        # Create a stream handler to print logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)  # You can set the desired log level for console output
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(console_handler)
        self._logger = logger

    @property
    def logger(self):
        return self._logger


logger = Logger().logger

def set_debug():
    global logger
    logger = Logger(level=logging.DEBUG)
