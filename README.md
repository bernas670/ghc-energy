# ghc-energy

## Software Versions
 - `ghc`: `8.8.4`
 - `python`: `3.10.6`

## Setup
### NoFib

Clone the [NoFib: Haskell Benchmark Suite](https://gitlab.haskell.org/ghc/nofib) and checkout to commit `bca0196`.
```
git clone https://gitlab.haskell.org/ghc/nofib.git nofib && \
cd nofib && \
git checkout bca0196 && \
cd ..
```

Switch `nofib`'s original `target.mk` for the modified version, which collects the execution time and energy consumption.
```
cp resources/target.mk nofib/mk/target.mk
```

Install the packages required by `nofib`'s benchmarks.
```
cabal v1-install --allow-newer -w ghc && \
cabal v1-install old-locale-1.0.0.7 old-time-1.1.0.3 parallel-3.2.2.0 primitive-0.7.4.0 random-1.2.1.1 regex-base-0.94.0.2 regex-compat-0.95.2.1 regex-posix-0.96.0.1 splitmix-0.1.0.4 unboxed-ref-0.4.0.0
```

Compile `runstdtest`.
```
cd nofib/runstdtest && make
```

### Tool
Install the tool requirements
```
pip3 install -r requirements.txt
```

Change the permissions of `/sys/class/powercap/intel-rapl` to allow all users to read this directory, removing the need to run anything with root priveleges.
```
sudo chmod -R a+r /sys/class/powercap/intel-rapl
```

## Usage
Before running the tool you must generate the input files for the benchmarks. Each benchmark has three different time `mode`s:
 - `fast`: 0.1 - 0.2 seconds
 - `norm`: 1 - 2 seconds
 - `slow`: 5 - 10 seconds
The default mode is `norm`, if you wish to change it you must do the following:
```
cd nofib && \
make clean && \
export mode=fast && \
make boot
```

To run the tool with the desired configurations change the `config.yaml` file (more details in [*Configuration*](#configuration)) and execute the command below.
```
python3 src/main.py
```

## Configuration

