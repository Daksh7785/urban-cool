import logging
import os
import config

def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger()
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(config.LOG_PATH, mode='w', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(log_format))
        logger.addHandler(fh)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(log_format))
        logger.addHandler(ch)

    return logger
