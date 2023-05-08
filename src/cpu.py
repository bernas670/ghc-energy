import subprocess
import multiprocessing
import sys
import time

from log import temperature_log

def cpu_temp() -> int:
    return int(subprocess.check_output(
        "sensors | grep -oE 'Package id [0-9]: * \\+[0-9]+\\.[0-9]+' | grep -oE '\\+[0-9]+\\.[0-9]+'",
        shell=True
    ).decode('ascii'))
    
def cpu_temperature() -> float:
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
        cpu_temperature = float(file.read().strip()) / 1000
    return cpu_temperature


def round_robin():
    """Functions to heat CPU 

    Based on the implementation of https://gist.github.com/ishan1608/87cb762f31b7af70a867 
    but capable of terminating when the temperature reaches a threshold
    """
    while(True):
        number = 0
        if(number >= sys.maxsize):
            number = 0
        else:
            number = number + 1


def heat_up_cpu(temperature, logfile=''):
    """Functions to heat CPU 

    Based on the implementation of https://gist.github.com/ishan1608/87cb762f31b7af70a867 
    but capable of terminating when the temperature reaches a threshold
    """
    process_cnt = 1
    processes = []
    q = multiprocessing.Queue()

    if logfile: temperature_log(False, logfile)
    # print("[CPU] - Heating up cpu")
    # print("[CPU] - Spawning Processes to to Heat up CPU")
    while(process_cnt <= multiprocessing.cpu_count()):
        temp = multiprocessing.Process(target=round_robin)
        processes.append(temp)
        temp.start()
        process_cnt += 1

    # print("[CPU] - Awaiting for spawned Processes to Finish or CPU temperature get high enough")
    cpu_temp = cpu_temperature()
    while (cpu_temp < temperature):
        cpu_temp = cpu_temperature()

    for process in processes:
        # print("[CPU] - Terminating process")
        process.terminate()

        if not process.is_alive():
            process.join(timeout=0.4)
            # print("[CPU] - Terminated process sucessfully joined")

    # time.sleep(0.1)
    if logfile: temperature_log(False, logfile, done=True, temp=cpu_temperature())
    # print(f"[CPU] - Finished heating up cpu. Currently at {cpu_temperature()}ºC")
    q.close()
      
    cool_down_cpu(temperature, logfile=logfile)

def cool_down_cpu(temperature, interval=0.15, logfile=''):
    if logfile: temperature_log(True, logfile)
    # print("[CPU] - Cooling down cpu")
    while cpu_temperature() > temperature:
        time.sleep(interval)
    if logfile: temperature_log(True, logfile, done=True, temp=cpu_temperature())
    # print(f"[CPU] - Finished cooling down cpu. Currently at {cpu_temperature()}ºC")
    