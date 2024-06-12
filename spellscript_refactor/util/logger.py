import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter to define the log format
format = "%(levelname)s:%(filename)s:%(lineno)03d:%(funcName)20s():%(message)s"
# format = "%(levelname)s:%(filename)s:%(funcName)s():%(message)s"
formatter = logging.Formatter(format)

# Create a file handler to write logs to a file
if logger.level != logging.INFO:
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Create a stream handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # You can set the desired log level for console output
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
