import logging
import os

import king_phisher
import king_phisher.client.plugins as plugins
import king_phisher.client.gui_utilities as gui_utilities

# logger name value
LOGGER_NAME = ''

class Plugin(plugins.ClientPlugin):
	authors = ['Zach Janice']
	title = 'Logger'
	description = """
	Keep logs of campaign feedback and results. The directory
	of the logged file(s), the file size (in MB) of the log, and
	the number of log files kept can be specified. Plugin requires
	the 'logging' and 'os' packages available for Python.
	"""
	req_packages = {}
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	options = []

	# this is the primary plugin entry point which is executed when the plugin is enabled
	def initialize(self):
		# ensure the directory for the logs exists
		log_dir = king_phisher.client.application.USER_DATA_PATH
		if not os.path.exists(log_dir):
			os.mkdir(log_dir)

		# sanitize the log file size option argument
		log_file_size = self.config['log_file_size']
		if log_file_size < 1:
			unsanitary_file_size_arg = True
			self.config['log_file_size'] = 1
			log_file_size = 1
		else:
			unsanitary_file_size_arg = False

		# sanitize the log file count option argument
		log_file_count = self.config['log_file_count']
		if log_file_count < 1:
			unsanitary_file_count_arg = True
			self.config['log_file_count'] = 1
			log_file_count = 1
		else:
			unsanitary_file_count_arg = False

		# convert the specified log file size (MB) to bytes for use by the logger
		file_size = log_file_size * 1024 * 1024

		# grab the logger in use by the client (root logger)
		logger = logging.getLogger(LOGGER_NAME)

		# set up the handler and formatter for the logger, and attach the components
		handler = logging.handlers.RotatingFileHandler("{0}/{1}".format(log_dir, 'client_log.log'), maxBytes=file_size, backupCount=log_file_count)
		formatter = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s: %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)

		# keep reference of handler as an attribute
		self.handler = handler

		# Report unsanitary input and resulting reversions, if applicable
		if unsanitary_file_size_arg:
			self.logger.warning("Invalid value for Logging plugin preference 'Log File Size' (below min value); reverting to min value of {0}".format(log_file_size))
		if unsanitary_file_count_arg:
			self.logger.warning("Invalid value for Logging plugin preference 'Log File Count' (below min value); reverting to min value of {0}".format(log_file_count))

		return True

	# this is a cleanup method to allow the plugin to close any open resources
	def finalize(self):
		# remove the logging handler from the logger and close it
		logger = logging.getLogger(LOGGER_NAME)
		logger.removeHandler(self.handler)
		self.handler.flush()
		self.handler.close()

