import os
import datetime
import logging
import logging.config
from pathlib import Path

from core import Core

LOG_FILE_NAME = '{}.log'.format(datetime.date.today().strftime('%Y%m%d'))
LOG_FILE_PATH = str(Path('./log') / LOG_FILE_NAME)
os.makedirs(Path(LOG_FILE_PATH).parent, exist_ok=True)


def setup_logger():
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'consoleHnadler',
                    'logFileHnadler',
                ]
            },
            'handlers': {
                'consoleHnadler': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'consoleFormatter',
                    'stream': 'ext://sys.stdout'
                },
                'logFileHnadler': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'formatter': 'logFileFormatter',
                    'filename': LOG_FILE_PATH,
                    'mode': 'a',
                    'encoding': 'utf-8'
                }
            },
            'formatters': {
                'consoleFormatter': {
                    'format': '[%(levelname)-8s]%(funcName)s -%(message)s'
                },
                'logFileFormatter': {
                    'format': '%(asctime)s|%(levelname)-8s|%(name)s|%(funcName)s|%(message)s'
                }
            }

        }
    )


if __name__ == '__main__':
    setup_logger()
    core = Core()
    core.run()
