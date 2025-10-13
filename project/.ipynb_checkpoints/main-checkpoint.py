import os
os.environ["ENERGYPLUS_EXE"] = "/project/lt200291-ignite/Project_chomwong/energyplus/EnergyPlus-25.1.0-1c11a3d85f-Linux-CentOS7.9.2009-2023-x86_64/energyplus"
os.environ["NCCL_DEBUG"] = "INFO"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TORCH_NCCL_TIMEOUT"] = "1200"
os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"

import yaml
import json
import pandas as pd
import torch
import torch.distributed as dist
import queue
import threading
from model import BuildingModel

def init_distributed():
    rank = int(os.environ.get("RANK", 0))
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    gpu_count = torch.cuda.device_count()

    if world_size > 1:
        backend = "nccl" if torch.cuda.is_available() and rank < gpu_count else "gloo"
        dist.init_process_group(
            backend=backend,
            rank=rank,
            world_size=world_size,
            init_method="env://"
        )
    else:
        backend = "gloo"

    device = torch.device(f"cuda:{rank}") if backend == "nccl" else torch.device("cpu")
    if backend == "nccl":
        torch.cuda.set_device(device)
    print(f"[Rank {rank}] Using backend={backend}, device={device}", flush=True)
    return rank, world_size, device, backend

def dict_to_tensor(d, keys, device):
    return torch.tensor([d.get(k, float('inf')) for k in keys], dtype=torch.float32, device=device)

def tensor_to_dict(tensor, keys):
    return {k: float(v) for k, v in zip(keys, tensor.tolist())}

def run_simulation():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    with open("agents.json", "r") as f:
        agents_json = json.load(f)

    rank, world_size, device, backend = init_distributed()
    steps = config["mesa"]["steps"]
    zone_keys = config["mesa"]["zones"]
    print("Zones:", zone_keys, flush=True)

    callback_queue = queue.Queue()

    model_agents = BuildingModel(config, "agents.json", ep_control=False)

    if rank == 0:
        model_agents.run_simulation_and_export(steps)

    ep_model = None
    if rank == 0:
        idf_path = "/project/lt200291-ignite/Project_chomwong/project/EnergyPlus_BP_Boonchoo/2ZoneDataCenterHVAC_wEconomizer.idf"
        weather_path = "/project/lt200291-ignite/Project_chomwong/project/EnergyPlus_BP_Boonchoo/DEU_BW_Stuttgart.AP.107380_TMYx.2009-2023.epw"
        ep_model = BuildingModel(config, ep_control=True, idf_path=idf_path)
        os.makedirs("outEnergyPlus", exist_ok=True)

        def ep_agent_callback(state):
            # Debug: confirm callback triggered
            print("[Callback] Triggered", flush=True)

            zone_temps = ep_model.read_zone_temps_from_ep()
            print("Current zone temperatures in EP:", flush=True)
            for zone, temp in zone_temps.items():
                print(f"  {zone}: {temp if temp is not None else 'N/A'}", flush=True)
            
            ep_model.last_zone_temps.update(zone_temps)
            
            callback_queue.put(zone_temps)
            #ep_model.step_agents(ep_model=ep_model)
            
            local_requests = ep_model.compute_setpoint_requests()

            ep_model.apply_setpoints_to_ep(local_requests)

            #callback_queue.put(local_requests)

        ep_model.api.runtime.callback_after_predictor_after_hvac_managers(
            ep_model.state, ep_agent_callback
        )

        ep_args = ["-d", "./outEnergyPlus", "-w", weather_path, idf_path]
        ep_thread = threading.Thread(target=lambda: ep_model.api.runtime.run_energyplus(ep_model.state, ep_args))
        ep_thread.start()
    for step in range(steps):
        if rank == 0:
            # รอ zone temps จาก EP callback
            zone_temps = callback_queue.get()  # block จน EP ส่งค่า
            model_agents.last_zone_temps.update(zone_temps)
    
            # อัพเดต agent → คำนวณ comfort_level และ AC decision
            model_agents.step_agents(ep_model=model_agents)
    
            # แสดงผล
            for agent in model_agents.schedule.agents:
                print(f"{agent.unique_id}: current_temp={agent.current_temp}, wants={agent.preferred_temp}, using_ac={agent.using_ac}", flush=True)
    
        # ส่ง setpoints ไป EP
        local_requests = model_agents.compute_setpoint_requests() if rank == 0 else {k: float('inf') for k in zone_keys}
        local_tensor = dict_to_tensor(local_requests, zone_keys, device)
    
        if world_size > 1:
            gathered = [torch.zeros_like(local_tensor) for _ in range(world_size)]
            dist.all_gather(gathered, local_tensor)
            merged_tensor = torch.min(torch.stack(gathered), dim=0).values
        else:
            merged_tensor = local_tensor
    
        merged_dict = tensor_to_dict(merged_tensor, zone_keys)
    
        if rank == 0 and ep_model:
            ep_model.apply_setpoints_to_ep(merged_dict)
            print("Applied setpoints to EP:", flush=True)
            for z, val in merged_dict.items():
                print(f"  {z}: {val:.2f} °C", flush=True)
    
        if (step + 1) % max(1, steps // 5) == 0:
            print(f"[Rank {rank}] Step {step+1}/{steps}", flush=True)
    
        if world_size > 1:
            dist.barrier()

    # for step in range(steps):
    #     if rank == 0:
    #         #model_agents.step_agents(ep_model)
    #         zone_temps = {z: ep_model.last_zone_temps.get(z, float('nan')) for z in zone_keys}
    #         for agent in model_agents.schedule.agents:
    #             print(f"{agent.unique_id}: current_temp={agent.current_temp}, wants={agent.preferred_temp}", flush=True)      
    #     local_requests = callback_queue.get() if rank == 0 else {k: float('inf') for k in zone_keys}
    #     local_tensor = dict_to_tensor(local_requests, zone_keys, device)

    #     if world_size > 1:
    #         gathered = [torch.zeros_like(local_tensor) for _ in range(world_size)]
    #         dist.all_gather(gathered, local_tensor)
    #         merged_tensor = torch.min(torch.stack(gathered), dim=0).values
    #     else:
    #         merged_tensor = local_tensor

    #     merged_dict = tensor_to_dict(merged_tensor, zone_keys)

    #     if rank == 0 and ep_model:
    #         ep_model.apply_setpoints_to_ep(merged_dict)
    #         print("Applied setpoints to EP:", flush=True)
    #         for z, val in merged_dict.items():
    #             print(f"  {z}: {val:.2f} °C", flush=True)

    #     if (step + 1) % max(1, steps // 5) == 0:
    #         print(f"[Rank {rank}] Step {step+1}/{steps}", flush=True)

    #     if world_size > 1:
    #         dist.barrier()

    if rank == 0 and ep_model:
        ep_thread.join()

    local_results = model_agents.collect_agent_results()
    if world_size > 1:
        dist.barrier()
        gathered_results = [None] * world_size
        dist.all_gather_object(gathered_results, local_results)
        if rank == 0:
            combined = []
            for sub in gathered_results:
                if sub:
                    combined.extend(sub)
            df = pd.DataFrame(combined)
            df.to_csv("mesa_agent_results.csv", index=False)
            print("[Rank 0] Results saved.", flush=True)
        dist.destroy_process_group()
    else:
        df = pd.DataFrame(local_results)
        df.to_csv("mesa_agent_results.csv", index=False)
        print("[Single rank] Results saved.", flush=True)

if __name__ == "__main__":
    run_simulation()