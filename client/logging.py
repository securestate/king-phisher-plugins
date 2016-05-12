import king_phisher.client.plugins as plugins
import king_phisher.client.gui_utilities as gui_utilities

try:
	import logging
except ImportError:
	has_logger = False # catch standard ImportError and set has_logger to False
else:
	has_logger = True # no errors, so logger has been imported

# default and minimum log file size values (in MB)
DEFAULT_LOG_SIZE = 10
MIN_LOG_SIZE = 0
LOG_FILE_COUNT = 2

# logger name and level values
LOGGER_NAME = 'KingPhisher'
DEFAULT_LOG_FILE_DIR = king_phisher.client.application.USER_DATA_PATH
LOG_FILE_NAME = 'client_log.log'

class Plugin(plugins.ClientPlugin):
	authors = ['Zach Janice']
	title = 'Logger'
	description = """
	Keep a log of campaign feedback and results. The file size
	(in MB) of the log can be specified. Plugin requires the
	logging package available for Python.
	"""
	req_packages {
		'logger': has_logger
	}
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	options = [
		plugins.ClientOptionString(
			'file_dir',
			'The directory to write the log file to.',
			default="{0}/{1}".format(DEFAULT_LOG_FILE_DIR, LOG_FILE_NAME),
			display_name='File Directory'
		),
		plugins.ClientOptionInteger(
			'log_size',
			'The size of the log to keep.',
			default=DEFAULT_LOG_SIZE,
			display_name='Log Size'
		)
	]

	# this is the primary plugin entry point which is executed when the plugin is enabled
	def initialize(self):
		# ensure a valid log file size in the config
		if self.config['log_size'] < MIN_LOG_SIZE:
			print("Log size parameter below minimum size; setting to default of {0}MB.".format(DEFAULT_LOG_SIZE))
			self.config['log_size'] = DEFAULT_LOG_SIZE

		# calculate the log file size (B) from the sanitized log size input (MB) and check for overflow
		log_file_size = self.config['log_size'] * 1024 * 1024
		if log_file_size < 0:
			print('WARNING: Log file size overflow; reverting to 1000B')
			log_file_size = 1000

		# create the directory for the log file if it does not exist
		if not os.path.exists(DEFAULT_LOG_FLE_DIR):
			os.makedir(DEFAULT_LOG_FILE_DIR)

		# grab the logger in use by the client (root logger)
		logger = logging.getLogger(LOGGER_NAME)

		# set up the handler and formatter for the logger, and attach the components
		handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes=log_file_size, backupCount=LOG_FILE_COUNT)
		formatter = logging.Formatter('%(asctime)s -- %(name) <%(levelname)>: %(message)')
		handler.setFormatter(formatter)
		logger.addHandler(handler)

		# Set level of logger to accept up to debug info
		logger.setLevel(logging.DEBUG)

	# this is a cleanup method to allow the plugin to close any open resources
	def finalize(self):
		# remove the logging handler from the logger and close it
		logger.removeHandler(handler)
		header.flush()
		header.close()

	def signal_exit(self, app):
		# code here
