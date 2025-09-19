#!/bin/bash
#SBATCH --job-name=mesa-cosim
#SBATCH --output=mesa-cosim.out
#SBATCH --error=mesa-cosim.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=4              # 1 process ต่อ 1 GPU
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:4            # ขอกี่ GPU ก็ใส่ตรงนี้
#SBATCH -p gpu
#SBATCH --mem=32G               # ปรับตามต้องการ
#SBATCH -A lt200291

module load cray-python/3.10.10

source ~/mesa_env/bin/activate

cd /project/lt200291-ignite/Project_chomwong/project

torchrun --standalone --nproc_per_node=4 main.py
