import sys
import os
import inspect
import logging
from loguru import logger


def setup_logger():
	sink_mode = 3

	

	custom_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

	logs_path = "logs/"

	logs_time_format = "{time:YYYY-MM-DD_HH-mm-ss}_"

	filters = {	"combined_logs": lambda record: True,
				"loguru_only_logs": lambda record: "name" not in record["extra"]}

	if sink_mode == 1:
		cli_sink = filters["loguru_only_logs"]
		level = "INFO"

	elif sink_mode == 2:
		cli_sink = filters["combined_logs"]
		level = "DEBUG"

	elif sink_mode == 3:
		cli_sink = filters["loguru_only_logs"]
		level = "TRACE"


	logger.remove(0)

	logger.add(sys.stderr, format=format, colorize=True, level=level, filter=cli_sink)

	logger.add(f"{logs_path}{logs_time_format}info_sink.log", format=custom_format, colorize=True, level="INFO", filter=filters["loguru_only_logs"])
	logger.add(f"{logs_path}{logs_time_format}debug_sink.log", format=custom_format, colorize=True, level="DEBUG", filter=filters["combined_logs"])
	logger.add(f"{logs_path}{logs_time_format}trace_sink.log", format=custom_format, colorize=True, level="TRACE", filter=filters["loguru_only_logs"])

	debug_logger = logger.bind(name=True)

	#---------------------- From loguru docs ----------------------#
	class InterceptHandler(logging.Handler):
		def emit(self, record: logging.LogRecord) -> None:
			# Get corresponding Loguru level if it exists.
			level: str | int
			try:
				level = logger.level(record.levelname).name
			except ValueError:
				level = record.levelno

			# Find caller from where originated the logged message.
			frame, depth = inspect.currentframe(), 0
			while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
				frame = frame.f_back
				depth += 1

			debug_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

	logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
	#---------------------- From loguru docs ----------------------#

def pytest_addoption(parser):
    ...

def pytest_configure(config):
	setup_logger()

def pytest_runtestloop(session):
	logger.info("test")
	logger.debug("test")
	logger.trace("test")
	logging.debug("debug test")

def pytest_collection_modifyitems(session, config, items):
	...


