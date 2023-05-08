import yaml
from ghc import compile
from services import ServiceManager

def file2array(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def main():
    
    # load config
    with open('config.yaml') as file:
        config = yaml.load(file, yaml.FullLoader)

    # read flags and progs
    flags = file2array(config['inputs']['flags'])
    progs = file2array(config['inputs']['benchmarks'])

    service_manager = ServiceManager()
    service_manager.disable()
    
    for prog in progs:
        for flag in flags:

            compile(prog, flag, config['number-of-executions'], config['base-flags'], config['outputs']['logs'])

    service_manager.enable()
    
if __name__ == "__main__":
    main()