import logging

from teams.log_config import log_format, log_level, log_date_format

#  log_file = "./teams.log"
#  logging.basicConfig(filename=log_file, filemode='w', format=log_format, level=log_level, datefmt=log_date_format)
logging.basicConfig(format=log_format, level=log_level, datefmt=log_date_format)