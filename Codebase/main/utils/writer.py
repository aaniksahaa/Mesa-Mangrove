import os
from utils.misc import clear_folder 

def clear_logs():
    folder_path = 'logs'
    clear_folder(folder_path)
    with open("logs/run_log.txt", 'w') as file:
        file.write('')

def run_log(text):
    with open("logs/run_log.txt", 'a') as file:
        file.write(str(text))
        file.write('\n')