'''Parse logs and put into readable format'''
from log_processes.get_logs import SearchForLog

class GetLogs:
    def __init__(self, *logs) -> None:
        self.logs = logs