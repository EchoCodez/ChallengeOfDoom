import logging as lg
from webbrowser import open_new_tab
from pathlib import Path

def setup_logging(log_file: Path = Path("logs/runlog.log"), logger_name = "CongressionalAppChallenge") -> lg.Logger:
    with open(log_file, "w"): # create file if it doesn't exist. Otherwise, clear file
        pass
    
    lg.basicConfig(
        format="%(asctime)s (%(filename)s) [L%(lineno)d] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    file_handler = lg.FileHandler(log_file)
    formatter = lg.Formatter(
        "%(asctime)s (%(filename)s) [L%(lineno)d] %(levelname)s: %(message)s", # L stands for line
        datefmt="%H:%M:%S"
        )
    
    file_handler.setFormatter(formatter)
    logger = lg.getLogger(logger_name)
    
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.setLevel(lg.DEBUG)
        
    return logger

def get_information_texts() -> tuple[dict[str, str | tuple]]:
    return (
        {
            "title": "Registering for APImedic",
            "content": "Congressional Health App uses the APImedic web api to rank which conditions you will be most likely to have based on your symptoms. \
                \nAs such, we need a username and password for APImedic. Don't worry, it's free! All you need to do is follow the instructions on the next page."
        },
        {
            "title": "Registering for APImedic",
            "content": "Just go through and follow the directions to sign up on the website (click the button below).\
                \nOnce you have completed the signup, login and go to \"API KEYS\" at the top bar of the website.\
                    \nThen click the arrow next to Live Basic API Account, and copy paste your username and password onto the next page.",
            "buttons": ("Go to website", "See registering live"),
            "commands": (lambda: open_new_tab("https://apimedic.com/signup"), lambda: open_new_tab("https://www.youtube.com/"))
        }
    )