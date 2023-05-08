import subprocess
import pyRAPL as rapl
import time
import yaml
import sys, os

from cpu import cpu_temperature, heat_up_cpu, cool_down_cpu
from ghc import get_info
from log import wrapper_log

def path(top, file):
    return f"{top}/{file}"

def micro2unit(value):
    return value * 1e-6

def main(top, command, program, flags):    
    # load config    
    with open(path(top, "config.yaml")) as file:
        config = yaml.load(file, yaml.FullLoader)
        
    # setup rapl
    rapl.setup()
    meter = rapl.Measurement('Energy Consumption')
    
    # warm-up / cooldown cpu
    base_temperature = config['temperature']['baseline']
    if cpu_temperature() > base_temperature:
        cool_down_cpu(base_temperature, logfile=path(top, config['outputs']['logs']))
    else:
        heat_up_cpu(base_temperature, logfile=path(top, config['outputs']['logs']))

    meter.begin()

    # run command and wait for it to finish
    process = subprocess.Popen(command, shell=True, 
                               stderr=subprocess.PIPE, 
                               stdout=subprocess.DEVNULL
                               )
    return_code = process.wait()

    meter.end()
    
    # log execution
    flag = flags[len(config['base-flags']):].strip()
    wrapper_log(program, flag, return_code, path(top, config['outputs']['logs']))
    
    # if error in execution don't store values
    if process.returncode != 0:
        os._exit(process.returncode)  
    
    # collect info provided by ghc
    ghc_output = process.stderr.read().decode()
    ghc_info = get_info(ghc_output)

    # write results to file
    with open(path(top, config['outputs']['results']), 'a') as file:
        # timestamp, program, flag, execution_time (µs), pkg_energy (µJ), dram_energy (µJ)
        file.write(f"{int(meter.result.timestamp)},{program},{flag},{process.returncode},{meter.result.duration},{meter.result.pkg[0]},{meter.result.dram[0]}")
        file.write(f",{','.join(ghc_info)}")
        file.write('\n')


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("[ERROR] Missing command-line arguments")
        pass
    
    # set stdout and stderr, because previously all output is redirected to /dev/null
    sys.stdout = open('/dev/tty', 'w')
    sys.stderr = open('/dev/tty', 'w')
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])