from logging import Logger

class SearchForLog:
    '''Class for working with log files'''
    def __init__(self, logger: Logger, name: str|None = None, date: str|None = None) -> None:
        if name is not None and date is not None:
            raise TypeError("Name and date cannot be provided at once")
        
        if name is not None:
            self.name = name
        else:
            self.name = f"json/logs/{date.replace('-', '_').replace('/', '_')}.json"
        
        self.logger = logger
    
    def search(self) -> list[dict] | dict:
        import json
        try:
            with open(self.name) as f:
                return json.load(f)
        except FileNotFoundError as e:
            return
            self.logger.debug(e)
        
