import logging as lg
from webbrowser import open_new_tab
from pathlib import Path
from utils import constants

def setup_logging(
    level: int = lg.DEBUG
) -> lg.Logger:
    
    log_file = constants.RUNLOG
    
    if not log_file.parent.exists(): # check if logs/ exists
        log_file.mkdir()
        
    with open(log_file, "w"): # create file if it doesn't exist. Otherwise, clear file
        pass
    _format = "%(asctime)s (%(filename)s) [L%(lineno)d] %(levelname)s: %(message)s"
    lg.basicConfig(
        format=_format,
        datefmt="%H:%M:%S"
    )
    file_handler = lg.FileHandler(log_file)
    formatter = lg.Formatter(
        _format, # L stands for line
        datefmt="%H:%M:%S"
        )
    
    file_handler.setFormatter(formatter)
    logger = constants.LOGGER
    
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.setLevel(level)
        
    return logger
