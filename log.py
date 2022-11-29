import sys
import os
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(f"{os.path.dirname(sys.argv[0])}{os.sep}work-log.log")
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


def add_warn(msg: str) -> None:
    try:
        logger.log(msg=msg, level=logging.WARNING)
    except Exception as err:
        logger.debug(msg=f'error in write log, {err}')
        logger.debug(msg=f'{__name__}, i want write msg: {msg}')


def add_to_log(msg: str) -> None:
    try:
        logger.log(msg=msg, level=logging.INFO)
    except Exception as err:
        logger.debug(msg=f'error in write log, {err}')
        logger.debug(msg=f'{__name__}, i want write msg: {msg}')
