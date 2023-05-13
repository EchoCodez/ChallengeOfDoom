from utils.parse_json import jsonUtils
import customtkinter as ctk


def set_theme() -> bool:
    '''Check if theme preference in file already.
    
    Returns:
    --------
        bool: whether or not appearance theme was found
    '''
    
    with open("json/preferences.json") as f:
        if jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode):
            return True
    return False

def delete_old_diagnosis(logger):
    from datetime import date
    
    logger.info("Attempting to save memory by deleting last months checkup results")
        
    current_date = date.today()
    current_month = current_date.month
    last_month = current_month - 1 if current_month != 1 else 12  
    today_a_month_ago = date(current_date.year, last_month, current_date.day).strftime("%d_%m_%y")
    
    last_months_checkup = f"json/logs/{today_a_month_ago}.json"
    try:
        jsonUtils.delete_file(last_months_checkup)
    except FileNotFoundError:
        logger.info(f"Last months checkup was not found. AKA file path {last_months_checkup} was not found.")
        return
    else:
        logger.info("Deletion of last months diagnosis was successfull")
    
    logger.info("Attempting to remove it from json/logs.json")
    
    try:
        data = jsonUtils.open("json/logs.json")["logs_list"]
        jsonUtils.overwrite(
            data = {"logs_list": [x for x in data if x != last_months_checkup]},
            file="json/logs.json"
            )
    except Exception as e:
        logger.warning(e)
    else:
        logger.info(f"Removed {last_months_checkup} from json/logs.json")
