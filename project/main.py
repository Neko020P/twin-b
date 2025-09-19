from model import BuildingModel
import yaml
import pandas as pd
import os
import torch
import torch.distributed as dist
from socket import gethostname

# ---------------------------
# ฟังก์ชัน helper DDP
# ---------------------------
def init_distributed(backend="nccl"):
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
    else:
        # fallback single-process
        rank = 0
        world_size = 1

    if world_size > 1:
        dist.init_process_group(
            backend=backend,
            rank=rank,
            world_size=world_size,
            init_method="env://"
        )
    return rank, world_size

def run_simulation():
    # ---------------------------
    # Initialize distributed
    # ---------------------------
    rank, world_size = init_distributed(backend="nccl" if torch.cuda.is_available() else "gloo")

    # Set device
    if torch.cuda.is_available():
        local_rank = rank % torch.cuda.device_count()
        torch.cuda.set_device(local_rank)
        device = torch.device(f"cuda:{local_rank}")
    else:
        device = torch.device("cpu")

    print(f"[Rank {rank}/{world_size}] Running on {device} ({gethostname()})", flush=True)

    # ---------------------------
    # Load config
    # ---------------------------
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # ---------------------------
    # Partition agents (optional)
    # ---------------------------
    total_agents = config["mesa"]["total_agents"]
    agents_per_rank = total_agents // world_size
    remainder = total_agents % world_size
    start = rank * agents_per_rank + min(rank, remainder)
    end = start + agents_per_rank + (1 if rank < remainder else 0)
    config["mesa"]["agent_ids"] = list(range(start, end))
    print(f"[Rank {rank}] Assigned agent IDs {config['mesa']['agent_ids'][:5]}{'...' if len(config['mesa']['agent_ids'])>5 else ''}", flush=True)

    # ---------------------------
    # Build model
    # ---------------------------
    model = BuildingModel(config)

    # ---------------------------
    # Run simulation
    # ---------------------------
    for step in range(config["mesa"]["steps"]):
        model.step()
        if (step + 1) % max(1, config["mesa"]["steps"] // 5) == 0:
            print(f"[Rank {rank}] Step {step+1}/{config['mesa']['steps']}", flush=True)

    # ---------------------------
    # Gather results from all ranks
    # ---------------------------
    local_results = model.agent_results  # list of dicts

    if world_size > 1:
        gathered = [None for _ in range(world_size)]
        dist.all_gather_object(gathered, local_results)
        if rank == 0:
            combined = []
            for sublist in gathered:
                if sublist:
                    combined.extend(sublist)
        dist.barrier()
        if rank == 0:
            df = pd.DataFrame(combined)
            df.to_csv("mesa_agent_results.csv", index=False)
            print(f"[Rank {rank}] Simulation finished. Results saved to mesa_agent_results.csv")
        dist.destroy_process_group()
    else:
        # single process
        df = pd.DataFrame(local_results)
        df.to_csv("mesa_agent_results.csv", index=False)
        print("Simulation finished. Results saved to mesa_agent_results.csv")

if __name__ == "__main__":
    run_simulation()
