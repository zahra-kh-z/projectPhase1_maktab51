import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('my_file.log')
logger.setLevel(logging.DEBUG)  # <<< Added Line
f_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.INFO)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(c_handler)  # for print in output
logger.addHandler(f_handler)

# for example
# logger.warning('This is a warning')
# logger.error('This is an error')
# logger.info('This is an info')

# logging without level
# logging.basicConfig(filename='my_file.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
