#!/bin/bash
#SBATCH --job-name=runEPlus
#SBATCH --output=/project/lt200291-ignite/Project_chomwong/test/runs/run6/log_%j.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00

# --- Path setup ---
RUN_NAME="run7"
BASE_DIR="/project/lt200291-ignite/Project_chomwong"
OUTPUT_DIR="$BASE_DIR/test/runs/$RUN_NAME"
INPUT_DIR="$BASE_DIR/test/inputs"
SCRIPT_DIR="$BASE_DIR/test/scripts"
EPLUS_BIN="$BASE_DIR/energyplus/EnergyPlus-25.1.0-1c11a3d85f-Linux-CentOS7.9.2009-x86_64/energyplus"

mkdir -p $OUTPUT_DIR

# --- 1) Run EnergyPlus ---
$EPLUS_BIN \
    -r \
    -x \ 
    -w $INPUT_DIR/weather/DEU_BW_Stuttgart.AP.107380_TMYx.2009-2023.epw \
    -d $OUTPUT_DIR \
    -p $RUN_NAME \
    $INPUT_DIR/idf/2ZoneDataCenterHVAC_wEconomizer.idf

echo "✅ EnergyPlus finished. Outputs are in $OUTPUT_DIR"

# --- 2) Post-process: convert ESO → CSV ---
module load Mako/1.2.4-cray-python-3.10.10   # หรือ conda activate ถ้าใช้ environment

python $SCRIPT_DIR/postprocess.py \
    --eso "$OUTPUT_DIR/${RUN_NAME}out.eso" \
    --out "$OUTPUT_DIR/${RUN_NAME}_temperature.csv"

echo "✅ Postprocessing finished. CSV is in $OUTPUT_DIR"



