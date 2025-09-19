#!/bin/bash
#SBATCH --job-name=csv_to_json
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2GB
#SBATCH --time=00:05:00
#SBATCH --output=convert_to_json_%j.out

module load cray-python/3.10.10
source ~/mesa_env/bin/activate

# แปลง energy_timeseries.csv -> energy_timeseries.json
python ~/project/csv_to_json.py --csv ~/project/outputs/energy_timeseries.csv \
                                 --json ~/project/outputs/energy_timeseries.json

# แปลง daily_summary.csv -> daily_summary.json
python ~/project/csv_to_json.py --csv ~/project/outputs/daily_summary.csv \
                                 --json ~/project/outputs/daily_summary.json
