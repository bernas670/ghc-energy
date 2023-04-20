import subprocess
import multiprocessing
import sys
import time

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


def heat_up_cpu(temperature):
    """Functions to heat CPU 

    Based on the implementation of https://gist.github.com/ishan1608/87cb762f31b7af70a867 
    but capable of terminating when the temperature reaches a threshold
    """
    process_cnt = 1
    processes = []
    q = multiprocessing.Queue()

    print("[CPU] - Spawning Processes to to Heat up CPU")
    while(process_cnt <= multiprocessing.cpu_count() or cpu_temperature() > temperature):
        temp = multiprocessing.Process(target=round_robin)
        processes.append(temp)
        temp.start()
        process_cnt += 1

    print("[CPU] - Awaiting for spawned Processes to Finish or CPU temperature get high enough")
    cpu_temp = cpu_temperature()
    while (cpu_temp < temperature):
        cpu_temp = cpu_temperature()

    for process in processes:
        print("[CPU] - Terminating process")
        process.terminate()

        if not process.is_alive():
            process.join(timeout=0.4)
            print("[CPU] - Terminated process sucessfully joined")

    print("[CPU] - Finished heating up cpu")
    q.close()

def cool_down_cpu(temperature, interval=5):
    while cpu_temperature() > temperature:
        print("[CPU] - Awaiting for cpu to cool down")
        time.sleep(interval)
    print("[CPU] - Finished cooling down")
    