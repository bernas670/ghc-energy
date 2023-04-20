import argparse
import pyRAPL as rapl
import subprocess
import time

from cpu import cpu_temperature, heat_up_cpu, cool_down_cpu



def main(command, program, flag):
    base_temp = 70
    res_file = 'results.csv'

    # initialize rapl
    rapl.setup()
    meter = rapl.Measurement('Energy Consumption')

    meter.begin()

    # run command
    process = subprocess.Popen(command, shell=True)
    process.wait()

    meter.end()

    print(f"Process terminated with return code: {process.returncode}")


    # warm-up / cooldown cpu
    if cpu_temperature() > base_temp:
        cool_down_cpu(base_temp)
    else:
        heat_up_cpu(base_temp)

    # write results to file
    with open(res_file, 'a') as file:
        # timestamp, program, flag, execution_time, pkg_energy, dram_energy
        file.write(f"{int(time.time())},{program},{flag},{meter.result.duration},{meter.result.pkg},{meter.result.dram}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('command', type=str, help='Description of arg1')
    parser.add_argument('program', type=str, help='Description of arg2')
    parser.add_argument('flag', type=str, help='Description of arg2')
    args = parser.parse_args()

    main(args.command, args.program, args.flag)