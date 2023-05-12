'''Parse logs and put into readable format'''
from log_processes.get_logs import SearchForLog
from log_processes.UI_health_log import get_previous_month

class GetLogs:
    def __init__(self, *logs) -> None:
        self.logs = logs

def main():
    x =SearchForLog(
        date="09/05/23"
    ).search()
    print(x)

if __name__ == "__main__":
    main()