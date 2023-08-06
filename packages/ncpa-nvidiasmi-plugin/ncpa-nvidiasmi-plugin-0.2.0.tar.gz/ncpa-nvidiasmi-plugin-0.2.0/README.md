# NCPA Nvidia-Smi Plugin

This NCPA plugin for checks Nvidia GPU stats for all GPUS detected via the nvidia-smi executable on linux machines

## Requirements

* Python 3.5 or greater
* nagiosplugin module - https://pypi.org/project/nagiosplugin/

## Setup

1. pip3 install nagiosplugin
2. install `check_nvidiasmi.py` into /usr/local/ncpa/plugins/check_nvidiasmi.py
3. ensure `/usr/local/ncpa/etc/ncpa.cfg` configured to use python3 binary for plugin scripts


## Usage 
```
usage: check_nvidiasmi.py [-h] [-a RANGE] [-A RANGE] [-u RANGE] [-U RANGE] [-m RANGE] [-M RANGE] [-t RANGE] [-T RANGE] [-p RANGE] [-P RANGE] [-v]

NCPA plugin to check Nvidia GPU status using nvidia-smi

optional arguments:
  -h, --help            show this help message and exit
  -a RANGE, --avg_gpu_warning RANGE
                        warning if threshold is outside RANGE for average of all GPUS
  -A RANGE, --avg_gpu_critical RANGE
                        critical if threshold is outside RANGE for average of all GPUS
  -u RANGE, --gpu_warning RANGE
                        warning if threshold is outside RANGE for any given GPU
  -U RANGE, --gpu_critical RANGE
                        critical if threshold is outside RANGE for any given GPU
  -m RANGE, --mem_warning RANGE
                        warning if threshold is outside RANGE for any given GPU
  -M RANGE, --mem_critical RANGE
                        critical if threshold is outside RANGE for any given GPU
  -t RANGE, --temp_warning RANGE
                        warning if threshold is outside RANGE for any given GPU
  -T RANGE, --temp_critical RANGE
                        critical if threshold is outside RANGE for any given GPU
  -p RANGE, --procs_warning RANGE
                        warning if threshold is outside RANGE for any given GPU
  -P RANGE, --procs_critical RANGE
                        critical if threshold is outside RANGE for any given GPU
  -v, --verbose         increase verbosity (use up to 3 times)
```