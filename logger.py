import logging
import os
import sys

import constant


class Logger:

    def __init__(self, custom_handler=None):
        """initialization
        """
        log_folder = os.path.join(constant.root_path, 'log')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        file_handler = logging.FileHandler(os.path.join(log_folder, 'chatapp.log'), mode='w', encoding='utf-8')

        if custom_handler is None:
            custom_handler = logging.StreamHandler(sys.stdout)

        custom_handler.setLevel(logging.INFO)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d | \t %(levelname)s:\t %(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[file_handler, custom_handler])

    def __call__(self, name: str):
        """get logger

        Args:
            name (str): logger name

        Returns:
            [logger]: get logger
        """
        return logging.getLogger(name)


log = (Logger())('chatapp')
