import argparse
import pyRAPL as rapl
import subprocess
import time
import yaml

from cpu import cpu_temperature, heat_up_cpu, cool_down_cpu


def path(top, file):
    return f"{top}/{file}"

def micro2unit(value):
    return value * 1e-6

def main(top, command, program, flag):
    # load config    
    with open(path(top, "config.yaml")) as file:
        config = yaml.load(file, yaml.FullLoader)
        
    # setup rapl
    rapl.setup()
    meter = rapl.Measurement('Energy Consumption')
    
    # warm-up / cooldown cpu
    base_temperature = config['temperature']['baseline']
    if cpu_temperature() > base_temperature:
        cool_down_cpu(base_temperature)
    else:
        heat_up_cpu(base_temperature)

    meter.begin()

    # run command
    process = subprocess.Popen(command, shell=True)
    process.wait()

    meter.end()

    print(f"Process terminated with return code: {process.returncode}")

    # write results to file
    with open(path(top, config['outputs']['results']), 'a') as file:
        # timestamp, program, flag, execution_time (µs), pkg_energy (µJ), dram_energy (µJ)
        file.write(f"{meter.result.timestamp},{program},{flag},{meter.result.duration},{meter.result.pkg[0]},{meter.result.dram[0]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('config_file', type=str, help='Description of arg1')
    parser.add_argument('command', type=str, help='Description of arg1')
    parser.add_argument('program', type=str, help='Description of arg2')
    parser.add_argument('flag', type=str, help='Description of arg2')
    args = parser.parse_args()

    main(args.config_file, args.command, args.program, args.flag)