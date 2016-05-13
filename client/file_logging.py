import king_phisher.client.plugins as plugins
import king_phisher.client.gui_utilities as gui_utilities

try:
	import logging
except ImportError:
	has_logger = False # catch standard ImportError and set has_logger to False
else:
	has_logger = True # no errors, so logger has been imported

try:
	import os
except ImportError:
	has_os = False #catch standard ImportError and set has_os to False
else:
	has_os = True # no errors, so os has been imported

# default and minimum log file size values (in MB)
LOG_FILE_SIZE = 10
LOG_FILE_COUNT = 2

# logger name and level values
LOGGER_NAME = ''
LOG_FILE_DIR = os.path.expanduser('~/.config/king-phisher/logs')
#LOG_FILE_DIR = os.path.expanduser('~/.config/king-phisher')
LOG_FILE_NAME = 'client_log.log'

class Plugin(plugins.ClientPlugin):
	authors = ['Zach Janice']
	title = 'Logger'
	description = """
	Keep a log of campaign feedback and results. The file size
	(in MB) of the log can be specified. Plugin requires the
	'logging' and 'os' packages available for Python.
	"""
	req_packages = {
		'logger': has_logger,
		'os': has_os
	}
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	options = []

	# this is the primary plugin entry point which is executed when the plugin is enabled
	def initialize(self):
		# convert the default log size (MB) to bytes for use by the logger
		file_size = LOG_FILE_SIZE * 1024 * 1024

		# create the directory for the log file if it does not exist
		if not os.path.exists(LOG_FILE_DIR):
			os.mkdir(LOG_FILE_DIR)

		# grab the logger in use by the client (root logger)
		logger = logging.getLogger(LOGGER_NAME)

		# set up the handler and formatter for the logger, and attach the components
		handler = logging.handlers.RotatingFileHandler("{0}/{1}".format(LOG_FILE_DIR, LOG_FILE_NAME), maxBytes=file_size, backupCount=LOG_FILE_COUNT)
		formatter = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s: %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)

		# keep reference of handler as an attribute
		self.handler = handler

		# Set level of logger to accept up to debug info
		logger.setLevel(logging.DEBUG)

		return True

	# this is a cleanup method to allow the plugin to close any open resources
	def finalize(self):
		# remove the logging handler from the logger and close it
		logger = logging.getLogger(LOGGER_NAME)
		logger.removeHandler(self.handler)
		self.handler.flush()
		self.handler.close()

