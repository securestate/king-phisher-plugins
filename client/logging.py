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

# logger name and level values
LOGGER_NAME = 'logger1'

class Plugin(plugins.ClientPlugin):
	authors = ['Zach Janice']
	title = 'Logger'
	description = """
	
	"""
	req_packages {
		'logger': has_logger
	}
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	options = [
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
	
		# instantiate the logger
		logger = logging.getLogger(LOGGER_NAME)
		self.logger = logger

		# determine if running in debug mode (?) and set the level of the logger accordingly
		if True:
			logger.setLevel(logging.DEBUG)
		else:
			logger.setLevel(logging.INFO)

	# this is a cleanup method to allow the plugin to close any open resources
	def finalize(self):
		# code here

	def signal_exit(self, app):
		# code here
