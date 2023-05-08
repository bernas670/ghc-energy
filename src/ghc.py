import os
import subprocess
import re
from log import compile_log, clean_log

def compile(path, flag, num_runs=1, base_flag='', logfile=''):
    root_dir = os.getcwd()
    
    try:
        os.chdir(f"./nofib/{path}")
        
        # compile (run command)
        process = subprocess.Popen(
                f"make NoFibRuns={num_runs} EXTRA_HC_OPTS=\"{base_flag} {flag}\"",
                # f"make NoFibRuns={num_runs} EXTRA_HC_OPTS=\"{base_flag} -package-db /home/user01/.ghc/x86_64-linux-8.10.7/package.conf.d {flag}\"",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return_code = process.wait()
        
        compile_log(path, flag, num_runs, return_code, f"{root_dir}/{logfile}")
        # print(f"[RET] - {'OK' if return_code == 0 else 'ERROR'} | '{path}' compiled with '{flag}' and executed {num_runs} times. Finished with return code: {return_code}")

        # make clean
        process = subprocess.Popen(
                "make clean",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return_code = process.wait()
        
        clean_log(path, return_code, f"{root_dir}/{logfile}")
        # TODO: log clean
        # print(f"[CLN] - {'OK' if return_code == 0 else 'ERROR'} | '{path}' cleaned {'un' if return_code else ''}sucessfully.\n")
        
        os.chdir(root_dir)
        
    except Exception as e:
        print(e)
        return -1
    
    return return_code


def get_values(input: str) -> list[str]:
    pattern = r"\d+[\.\d+|:\d+\.\d+]*"
    return re.findall(pattern, input)

def get_info(output_str: str) -> list[str]:
    cpu_line, mem_line, ghc_line = output_str.strip().split('\n')
    
    # cpu info
    user_time, sys_time, total_time, cpu_percent, avg_text, avg_data, peak_rss = get_values(cpu_line)
    
    # convert total_time to float
    minutes, seconds = total_time.split(':')
    total_time = str(int(minutes) * 60 + float(seconds))
    
    cpu_info = [user_time, sys_time, total_time, cpu_percent, avg_text, avg_data, peak_rss]
    
    # mem info
    inputs, outputs, minor_pagefaults, major_pagefaults, swaps = get_values(mem_line)
    mem_info = [inputs, outputs, minor_pagefaults, major_pagefaults, swaps]

    # ghc info
    ghc_values = get_values(ghc_line)
    alloc_mem, reclaimed_mem, rts_mem = ghc_values[0], *ghc_values[7:9]
    total_gcs, minor_gcs, major_gcs = ghc_values[1:4]
    avg_mem, max_mem, n_samples = ghc_values[4:7]
    init_cpu, init_sys, mut_cpu, mut_sys, total_gc_cpu, total_gc_sys = ghc_values[9:15]
    minor_gc_cpu, minor_gc_sys, major_gc_cpu, major_gc_sys = *ghc_values[15:18:2], *ghc_values[18:21:2] 
    balance = ghc_values[21]
    
    ghc_info = [alloc_mem, reclaimed_mem, rts_mem, total_gcs, minor_gcs, major_gcs,
                avg_mem, max_mem, n_samples, 
                init_cpu, init_sys, mut_cpu, mut_sys, total_gc_cpu, total_gc_sys,
                minor_gc_cpu, minor_gc_sys, major_gc_cpu, major_gc_sys, balance]
    
    return [*cpu_info, *mem_info, *ghc_info]