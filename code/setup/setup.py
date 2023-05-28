import logging as lg
from setup.setup_questions import Questions
from log.health_log import Calendar

def setup_logging(log_file: str = "logs/runlog.log", logger_name = __name__) -> lg.Logger:
    with open(log_file, "w"): # create file if it doesn't exist. Otherwise, clear file
        pass
    
    lg.basicConfig(
        format="%(asctime)s (%(filename)s) %(name)s: %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = lg.FileHandler(log_file)
    formatter = lg.Formatter(
        "%(asctime)s (%(filename)s) %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    file_handler.setFormatter(formatter)
    logger = lg.getLogger(logger_name)
    
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.setLevel(lg.DEBUG)
        
    return logger