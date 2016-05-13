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

# default values for configuration options
DEFAULT_LOG_DIR = os.path.expanduser('~/.config/king-phisher/logs')
DEFAULT_LOG_FILE_SIZE = 10
DEFAULT_LOG_FILE_COUNT = 2

# minimum integer option values
MIN_LOG_FILE_SIZE = 1
MIN_LOG_FILE_COUNT = 1

# logger name and file name values
LOGGER_NAME = ''
LOG_FILE_NAME = 'client_log.log'

class Plugin(plugins.ClientPlugin):
	authors = ['Zach Janice']
	title = 'Logger'
	description = """
	Keep logs of campaign feedback and results. The directory
	of the logged file(s), the file size (in MB) of the log, and
	the number of log files kept can be specified. Plugin requires
	the 'logging' and 'os' packages available for Python.
	"""
	req_packages = {
		'logger': has_logger,
		'os': has_os
	}
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	options = [
		plugins.ClientOptionString(
			'log_dir',
			'The directory in which to create the log file(s).',
			default=DEFAULT_LOG_DIR,
			display_name='Log Directory'
		),
		plugins.ClientOptionInteger(
			'log_file_size',
			'The maximum size, in megabytes, of a single log file.',
			default=DEFAULT_LOG_FILE_SIZE,
			display_name='Log File Size (MB)'
		),
		plugins.ClientOptionInteger(
			'log_file_count',
			'The number of log files that will be maintained by the plugin.',
			default=DEFAULT_LOG_FILE_COUNT,
			display_name='Number of Log Files'
		)
	]

	# this is the primary plugin entry point which is executed when the plugin is enabled
	def initialize(self):
		log_dir = self.config['log_dir']
		if not os.path.isdir(log_file_dir):
			unsanitary_log_dir = True
			self.config['log_dir'], log_dir = DEFAULT_LOG_DIR
		else:
			unsanitary_log_dir = False

		# sanitize the log file size option argument
		log_file_size = self.config['log_file_size']
		if log_file_size < MIN_LOG_FILE_SIZE:
			unsanitary_file_size_arg = True
			self.config['log_file_size'], log_file_size = MIN_LOG_FILE_SIZE
		else:
			unsanitary_file_size_arg = False

		# sanitize the log file count option argument
		log_file_count = self.config['log_file_count']
		if log_file_count < MIN_LOG_FILE_COUNT:
			unsanitary_file_count_arg = True
			self.config['log_file_count'], log_file_size = MIN_LOG_FILE_COUNT
		else:
			unsanitary_log_file_count = False

		# convert the specified log file size (MB) to bytes for use by the logger
		file_size = log_file_size * 1024 * 1024

		# create the directory for the log file if it does not exist
		if not os.path.exists(log_file_dir):
			os.mkdir(log_file_dir)

		# grab the logger in use by the client (root logger)
		logger = logging.getLogger(LOGGER_NAME)

		# set up the handler and formatter for the logger, and attach the components
		handler = logging.handlers.RotatingFileHandler("{0}/{1}".format(log_dir, LOG_FILE_NAME), maxBytes=file_size, backupCount=log_file_count)
		formatter = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s: %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)

		# keep reference of handler as an attribute
		self.handler = handler

		# Set level of logger to accept up to debug info
		logger.setLevel(logging.DEBUG)

		# Report unsanitary input and resulting reversions, if applicable
		if unsanitary_log_dir:
			logger.warning("Invalid directory specified for Logging plugin preference 'Log Directory' (not a directory); reverting to default directory of {0}".format(log_dir))
		if unsanitary_file_size_arg:
			logger.warning("Invalid value for Logging plugin preference 'Log File Size' (below min value); reverting to min value of {0}".format(log_file_size))
		if unsanitary_file_count_arg:
			logger.warning("Invalid value for Logging plugin preference 'Log File Count' (below min value); reverting to min value of {0}".format(log_file_count))

		return True

	# this is a cleanup method to allow the plugin to close any open resources
	def finalize(self):
		# remove the logging handler from the logger and close it
		logger = logging.getLogger(LOGGER_NAME)
		logger.removeHandler(self.handler)
		self.handler.flush()
		self.handler.close()

