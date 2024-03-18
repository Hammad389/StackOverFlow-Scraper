import os.path
from platform import system as system_platform
from os import system, path
from os.path import isfile
from psutil import Process


class Pprints:

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    MAGENTA = '\033[35m'

    def __init__(self) -> None:
        self._process = Process()
        self._log_file = 'logs.txt'
        self._database_file_size = './database/python_question_answers_snippets.db'

    @staticmethod
    def clean_terminal() -> str:
        if system_platform() == 'Windows':
            system('cls')
        else:
            system('clear')
        return system_platform()

    def pretty_prints(self, status: str, log: bool = False) -> None:
        memory_info = self._process.memory_info()
        current_memory_usage = memory_info.rss / 1024 / 1024
        database_file_size = os.path.getsize(self._database_file_size)
        current_database_file_size = round(database_file_size/1000/1000, 2)
        non_log_msg = f"Status: {status}\n"
        log_msg = f"{self.GREEN}Platform: {self.clean_terminal()}\n" \
                  f"{self.CYAN}Developer: HAMMAD\n" \
                  f"{self.GREEN}StackOverFlow Scraper Version: 0.1\n" \
                  f"{self.WARNING}GitHub: github.com/Hammad389\n" \
                  f"{self.MAGENTA}Status: {status}\n" \
                  f"{self.GREEN}Database File(sqlite3) size: {current_database_file_size}MB:\n" \
                  f"{self.WARNING}MemoryUsageByScript: {current_memory_usage: .2f}MB\n" \
                  f"{self.RED}Warning: Don't open the output file while script is running\n{self.RESET}"
        print(log_msg)
        if log:
            if isfile(self._log_file):
                file_obj = open(self._log_file, 'a')
                file_obj.write(non_log_msg)
                file_obj.close()
            else:
                file_obj = open(self._log_file, 'w')
                file_obj.write(non_log_msg)
                file_obj.close()
