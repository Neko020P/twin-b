#!/bin/bash
#SBATCH --job-name=extract_zone_temp
#SBATCH --output=extract_zone_temp_%j.log
#SBATCH --error=extract_zone_temp_%j.err
#SBATCH --time=00:10:00
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G


module load Mako/1.2.4-cray-python-3.10.10


export CSV_FILE="/path/to/2ZoneDataCenterHVAC_wEconomizer.csv"
export OUTPUT_FILE="/path/to/2Zone_TempOnly.csv"


python3 extract_zone_temp.py
