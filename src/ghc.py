import os
import subprocess

def compile(path, flag, num_runs=1):
    root_dir = os.getcwd()
    print(f"root dir: {root_dir}")
    
    try:
        os.chdir(f"./nofib/{path}")
        
        # compile (run command)
        process = subprocess.Popen(
                f"make NoFibRuns={num_runs} EXTRA_HC_OPTS=\"-O2 {flag}\"",
                shell=True
            )
        return_code = process.wait()
        print(f"Process finished with return code: {return_code}")

        # make clean
        process = subprocess.Popen("make clean >null 2>null", shell=True)
        # TODO: log clean
        
        os.chdir(root_dir)
        
    except Exception as e:
        print(e)
        return -1
    
    return return_code