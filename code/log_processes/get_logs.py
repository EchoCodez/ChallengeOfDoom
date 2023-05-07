class SearchForLog:
    '''Class for working with log files'''
    def __init__(self, name: str = None, date: str|None = None) -> None:
        if name is None and date is None or name is not None and date is not None:
            raise TypeError("Name and date cannot be provided at once")
        
        if name is not None:
            self.name = name
        else:
            self.data = f"logs/{date.replace('-', '_').replace('/', '_')}.log"
