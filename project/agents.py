#!/usr/bin/env python3
"""
Distributed Mesa simulation using PyTorch process group for sync/collect.

Run example (4 processes on one node):
torchrun --nproc_per_node=4 distributed_mesa.py --total-agents 100 --steps 50 --zones "A,B,C,D"
"""

import argparse
import os
import random
import csv
from socket import gethostname

import torch
import torch.distributed as dist

from mesa import Agent, Model

# ---------------------------
# Agent classes (user provided)
# ---------------------------
class StudentAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.role = "student"
        self.preferred_temp = random.uniform(24, 26)
        self.comfort_tolerance = random.uniform(1.5, 2.5)
        self.current_room = random.choice(model.config["mesa"]["zones"])

    def step(self):
        temp = self.model.get_current_temp(self.current_room)
        if temp is not None:
            using_ac = temp > self.preferred_temp
            comfort_level = abs(temp - self.preferred_temp)
            self.model.agent_results.append({
                "step": self.model.current_step,
                "agent_id": self.unique_id,
                "agent_type": self.role,
                "room": self.current_room,
                "comfort_level": round(comfort_level, 2),
                "using_ac": using_ac,
                "preferred_temp": round(self.preferred_temp, 2)
            })

class StaffAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.role = "staff"
        self.preferred_temp = random.uniform(25, 27)
        self.comfort_tolerance = random.uniform(1, 2)
        self.current_room = random.choice(model.config["mesa"]["zones"])

    def step(self):
        temp = self.model.get_current_temp(self.current_room)
        if temp is not None:
            using_ac = temp > self.preferred_temp
            comfort_level = abs(temp - self.preferred_temp)
            self.model.agent_results.append({
                "step": self.model.current_step,
                "agent_id": self.unique_id,
                "agent_type": self.role,
                "room": self.current_room,
                "comfort_level": round(comfort_level, 2),
                "using_ac": using_ac,
                "preferred_temp": round(self.preferred_temp, 2)
            })

class CleanerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.role = "cleaner"
        self.preferred_temp = random.uniform(26, 28)
        self.comfort_tolerance = random.uniform(2.5, 3.5)
        self.route = model.config["mesa"]["zones"]
        self.current_room = self.route[0]

    def step(self):
        temp = self.model.get_current_temp(self.current_room)
        if temp is not None:
            using_ac = temp > self.preferred_temp
            comfort_level = abs(temp - self.preferred_temp)
            self.model.agent_results.append({
                "step": self.model.current_step,
                "agent_id": self.unique_id,
                "agent_type": self.role,
                "room": self.current_room,
                "comfort_level": round(comfort_level, 2),
                "using_ac": using_ac,
                "preferred_temp": round(self.preferred_temp, 2)
            })
        # move to next room
        self.current_room = self.route[(self.route.index(self.current_room)+1) % len(self.route)]

class WardenAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.role = "warden"
        self.preferred_temp = random.uniform(25, 27)
        self.comfort_tolerance = random.uniform(2, 3)
        self.current_room = random.choice(model.config["mesa"]["zones"])

    def step(self):
        temp = self.model.get_current_temp(self.current_room)
        if temp is not None:
            using_ac = temp > self.preferred_temp
            comfort_level = abs(temp - self.preferred_temp)
            self.model.agent_results.append({
                "step": self.model.current_step,
                "agent_id": self.unique_id,
                "agent_type": self.role,
                "room": self.current_room,
                "comfort_level": round(comfort_level, 2),
                "using_ac": using_ac,
                "preferred_temp": round(self.preferred_temp, 2)
            })

class VisitorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.role = "visitor"
        self.preferred_temp = random.uniform(24, 26)
        self.comfort_tolerance = random.uniform(1, 1.5)
        self.current_room = random.choice(model.config["mesa"]["zones"])

    def step(self):
        temp = self.model.get_current_temp(self.current_room)
        if temp is not None:
            using_ac = temp > self.preferred_temp
            comfort_level = abs(temp - self.preferred_temp)
            self.model.agent_results.append({
                "step": self.model.current_step,
                "agent_id": self.unique_id,
                "agent_type": self.role,
                "room": self.current_room,
                "comfort_level": round(comfort_level, 2),
                "using_ac": using_ac,
                "preferred_temp": round(self.preferred_temp, 2)
            })

# ---------------------------
# Simple Mesa-like Model
# ---------------------------
class SimpleBuildingModel(Model):
    def __init__(self, config, agent_id_list):
        super().__init__()  # ✅ แก้คำเตือนตรงนี้
        self.config = config
        self.current_step = 0
        self.agent_results = []
        self.agents = []
        self._build_agents(agent_id_list)

    def _build_agents(self, agent_id_list):
        # create agents with types (rotate through types for demo)
        types = [StudentAgent, StaffAgent, CleanerAgent, WardenAgent, VisitorAgent]
        for idx, uid in enumerate(agent_id_list):
            cls = types[idx % len(types)]
            a = cls(uid, self)
            self.agents.append(a)

    def get_current_temp(self, room):
        # placeholder: return deterministic or randomized temperatures per room
        # For reproducibility, use a simple hash:
        return 24.0 + (hash(room) % 100) / 50.0  # yields temperatures roughly 24.0..26.98

    def step(self):
        self.current_step += 1
        # step all agents (synchronous)
        for a in self.agents:
            a.step()

# ---------------------------
# Distributed utilities
# ---------------------------
def init_distributed(args):
    # prefer environment-driven init (torchrun sets envs)
    # fallback to explicit args
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
    else:
        rank = args.rank
        world_size = args.world_size

    backend = args.backend
    # init_method uses env:// to let torchrun handle rendezvous
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size, init_method="env://")
    return rank, world_size

def partition_agent_ids(total_agents, world_size, rank):
    """
    Partition agent unique IDs (0..total_agents-1) across ranks as evenly as possible.
    Returns list of unique_ids assigned to this rank.
    """
    ids = list(range(total_agents))
    # simple block partitioning with remainder
    per_rank = total_agents // world_size
    remainder = total_agents % world_size
    start = rank * per_rank + min(rank, remainder)
    end = start + per_rank + (1 if rank < remainder else 0)
    return ids[start:end]

# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--total-agents", type=int, default=100, help="total number of agents across all processes")
    parser.add_argument("--steps", type=int, default=50, help="number of simulation steps")
    parser.add_argument("--zones", type=str, default="ZoneA,ZoneB", help="comma-separated zone names")
    parser.add_argument("--backend", type=str, default="gloo", help="dist backend (gloo/nccl)")
    # if not using torchrun/torch.distributed envs, you can pass rank/world_size via args (not typical)
    parser.add_argument("--rank", type=int, default=0, help="rank (if not using env RANK)")
    parser.add_argument("--world-size", type=int, default=1, help="world_size (if not using env WORLD_SIZE)")
    parser.add_argument("--out", type=str, default="distributed_results.csv", help="output CSV (rank 0 writes)")
    args = parser.parse_args()

    # initialize distributed
    rank, world_size = init_distributed(args)
    hostname = gethostname()
    print(f"[rank {rank}/{world_size}] started on {hostname}", flush=True)

    # set per-rank seed for reproducibility (optional)
    seed = 1234 + rank
    random.seed(seed)

    # config
    zones = [z.strip() for z in args.zones.split(",") if z.strip()]
    config = {"mesa": {"zones": zones}}

    # partition agent IDs
    my_agent_ids = partition_agent_ids(args.total_agents, world_size, rank)
    print(f"[rank {rank}] assigned {len(my_agent_ids)} agents (ids {my_agent_ids[:5]}{ '...' if len(my_agent_ids)>5 else '' })", flush=True)

    # build model for this rank
    model = SimpleBuildingModel(config=config, agent_id_list=my_agent_ids)

    # run simulation
    for step in range(args.steps):
        model.step()
        # optionally print per-rank progress periodically
        if (step + 1) % max(1, args.steps // 5) == 0 and rank == 0:
            print(f"[rank {rank}] step {step+1}/{args.steps}", flush=True)

    # gather results from all ranks
    local_results = model.agent_results  # Python list of dicts

    # Use all_gather_object to collect lists from all ranks
    gathered = [None for _ in range(world_size)]
    dist.all_gather_object(gathered, local_results)

    # only rank 0 combines and writes CSV
    if rank == 0:
        # flatten
        combined = []
        for sublist in gathered:
            if sublist:
                combined.extend(sublist)
        # sort by step then agent_id for stable order
        combined.sort(key=lambda d: (d["step"], d["agent_id"]))
        # write CSV
        fieldnames = ["step", "agent_id", "agent_type", "room", "comfort_level", "using_ac", "preferred_temp"]
        with open(args.out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in combined:
                writer.writerow(row)
        print(f"[rank {rank}] wrote combined results ({len(combined)} rows) to {args.out}", flush=True)

    # cleanup
    dist.barrier()
    dist.destroy_process_group()

if __name__ == "__main__":
    main()
