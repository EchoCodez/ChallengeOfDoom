import logging as lg

def setup_logging(log_file: str = "logs/runlog.log") -> lg.Logger:
    level = lg.DEBUG
    
    with open(log_file, "w"): # create file if it doesn't exist. Otherwise, clear file
        pass
    
    lg.basicConfig(
        level=level,
        format="%(asctime)s (%(filename)s) %(name)s: %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = lg.FileHandler(log_file)
    formatter = lg.Formatter("%(asctime)s (%(filename)s) %(name)s: %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    logger = lg.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger