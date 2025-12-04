# utils/color_log_formatter.py
import logging

RESET = "\033[0m"
COLOR_INFO = "\033[32m"      # Verde
COLOR_WARNING = "\033[33m"   # Amarillo
COLOR_ERROR = "\033[31m"     # Rojo
COLOR_DEBUG = "\033[34m"     # Azul

class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: COLOR_DEBUG + "%(asctime)s [%(levelname)s] %(message)s" + RESET,
        logging.INFO: COLOR_INFO + "%(asctime)s [%(levelname)s] %(message)s" + RESET,
        logging.WARNING: COLOR_WARNING + "%(asctime)s [%(levelname)s] %(message)s" + RESET,
        logging.ERROR: COLOR_ERROR + "%(asctime)s [%(levelname)s] %(message)s" + RESET,
        logging.CRITICAL: COLOR_ERROR + "%(asctime)s [%(levelname)s] %(message)s" + RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)
