import yaml
from ghc import compile


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

    # TODO: disable services

    for prog in progs:
        for flag in flags:

            compile(prog, flag, config['number-of-executions'])

    # TODO: enable services
    
if __name__ == "__main__":
    main()