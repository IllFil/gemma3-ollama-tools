import logging

def setup_logging(log_file: str = 'chat_log.log'):
    """
    Setup logging to a specified log file.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file,
        filemode='w'
    )