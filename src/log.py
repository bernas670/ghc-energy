from datetime import datetime
from enum import Enum

def wrapper_log(program: str, flag: str, ret: int, logfile: str):
    header = "RUN"
    message = f"{'OK' if ret == 0 else 'ERROR':<5} | '{program}' compiled with '{flag}' terminated with return code: {ret}"
    
    log(header, message, logfile)
    
def compile_log(path, flag, num_runs, ret, logfile):
    header = "CMP"
    message = f"{'OK' if ret == 0 else 'ERROR':<5} | '{path}' compiled with '{flag}' and executed {num_runs} times. Finished with return code: {ret}"
    
    log(header, message, logfile)

def clean_log(path, ret, logfile):
    header = "CLN"
    message = f"{'OK' if ret == 0 else 'ERROR':<5} | '{path}' cleaned {'un' if ret else ''}sucessfully.\n"
    
    log(header, message, logfile)

def temperature_log(cooling: bool, logfile: str, done=False, temp=None):
    header = "CPU"
    
    if done: message = f"Finished {'cooling down' if cooling else 'heating up'} cpu. Currently at {temp}ºC."
    else: message = f"{'Cooling down' if cooling else 'Heating up'} cpu"
    
    log(header, message, logfile)

def log(header: str, message: str, logfile: str, cmd=True):
    text = f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")}] [{header}] - {message}'
    
    if cmd: print(text)
        
    with open(logfile, 'a') as file:
        file.write(f"{text}\n")
