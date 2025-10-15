# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Building Energy Co-Simulation System** that couples agent-based modeling (Mesa) with building energy simulation (EnergyPlus). The system simulates occupant thermal comfort preferences and their interaction with HVAC systems in a multi-zone building environment.

### Core Architecture

The simulation architecture integrates three main components:

1. **Mesa Agent-Based Model (ABM)** - Simulates building occupants with individual thermal preferences
2. **EnergyPlus Building Simulation** - Simulates physical building thermal dynamics and HVAC systems
3. **PyTorch Distributed Data Parallel (DDP)** - Enables distributed computing across multiple processes/GPUs

#### Communication Flow

```
Mesa Agents → compute_setpoint_requests() → PyTorch DDP (all_gather)
    → merge setpoints (min) → apply_setpoints_to_ep() → EnergyPlus
    → EP callback → read_zone_temps_from_ep() → update agents → repeat
```

The coupling happens through:
- **EnergyPlus callbacks**: `callback_after_predictor_after_hvac_managers` triggers after each HVAC timestep
- **EnergyPlus API handles**: Temperature variables and cooling setpoint actuators for each zone
- **Queue-based synchronization**: Python `queue.Queue()` coordinates between EP thread and main simulation loop

### Key Components

#### 1. Agent Types (`agent.py`)
All agents inherit from `BaseAgent` with thermal comfort logic:
- `StudentAgent`, `StaffAgent`, `CleanerAgent`, `WardenAgent`, `VisitorAgent`, `PolicyAgent`
- Each agent has: `preferred_temp`, `comfort_tolerance`, `current_room`, `using_ac`
- Agent behavior: `using_ac = abs(current_temp - preferred_temp) > comfort_tolerance`

#### 2. Building Model (`model.py`)
The `BuildingModel` class handles both Mesa-only and EnergyPlus-coupled modes:
- **Mesa mode** (`ep_control=False`): Standalone agent simulation
- **EnergyPlus mode** (`ep_control=True`): Coupled co-simulation with EP API

Key methods:
- `step_agents()`: Updates agent states based on current zone temperatures
- `compute_setpoint_requests()`: Aggregates AC requests from agents (returns min temp per zone)
- `read_zone_temps_from_ep()`: Retrieves zone temperatures via EnergyPlus API handles
- `apply_setpoints_to_ep()`: Sends cooling setpoints to EnergyPlus via actuators

#### 3. Main Simulation Loop (`main.py`)
Orchestrates the co-simulation with distributed computing:
- Initializes PyTorch DDP (NCCL for GPU, Gloo for CPU)
- Runs EnergyPlus in separate thread on rank 0
- Synchronizes setpoint requests across distributed processes using `torch.distributed.all_gather`
- Merges requests with `torch.min()` (most aggressive cooling wins)

#### 4. Agent Configuration (`agents.json`)
Defines agent populations with statistical distributions:
- `count`: Number of agents per type
- `gender_ratio`, `age_range`: Demographics
- `preferred_temp`: Temperature preference distribution (uniform/normal)
- `comfort_tolerance`: Tolerance for temperature deviation

#### 5. Configuration (`config.yaml`)
Simulation parameters:
- `steps`: Number of simulation timesteps (typically 288 = 24h at 5min intervals)
- `zones`: List of building zones (must match EnergyPlus IDF zone names)
- `agents_file`: Path to agent configuration JSON

## Common Commands

### Running Simulations

**Single-process Mesa-only simulation:**
```bash
python project/main.py
```

**Multi-process distributed simulation (local):**
```bash
torchrun --standalone --nproc_per_node=2 project/main.py
```

**SLURM cluster submission:**
```bash
sbatch project/job.slurm
```

### Environment Setup

The project uses a Python virtual environment with specific EnergyPlus paths. Key environment variables set in `main.py`:
- `ENERGYPLUS_EXE`: Path to EnergyPlus executable
- `OMP_NUM_THREADS`: Set to 1 to avoid threading conflicts
- `TORCH_NCCL_TIMEOUT`: Timeout for distributed operations (1200s)

### Output Files

Simulations generate:
- `mesa_agent_results.csv`: Agent-level results (comfort, temperature, AC usage per timestep)
- `zone_results.csv`: Zone-level aggregated results
- `outEnergyPlus/`: EnergyPlus output directory with standard EP outputs

### Analysis

Jupyter notebooks in `project/analyze/` contain post-processing:
- Zone temperature analysis
- Agent comfort level statistics
- Policy evaluation comparisons

## Development Notes

### Zone Name Mapping

The code normalizes zone names (lowercase, underscore replacement) to match between Mesa config and EnergyPlus IDF:
- Mesa config: `"West Zone"`
- EnergyPlus IDF: `"WEST ZONE"`
- Normalized: `"west_zone"`

This mapping is critical in `model.py:56-61` - if zones don't match, handles will be -1 and communication fails.

### Distributed Computing Logic

Only rank 0 runs EnergyPlus and Mesa agents. Other ranks:
- Send `float('inf')` for their setpoint requests
- Participate in `all_gather` to receive merged setpoints
- Contribute to distributed barrier synchronization

The `torch.min()` aggregation ensures the coolest requested temperature wins across all ranks.

### EnergyPlus API Handle Initialization

Handles must be obtained during the first timestep callback (not at initialization) because the EnergyPlus state isn't fully initialized until runtime. The `setup_handles_first_timestep` callback pattern is essential.

### Thread Safety

The EnergyPlus simulation runs in a separate thread (`ep_thread`). The main loop uses `callback_queue.get()` (blocking) to synchronize with EP callbacks. This ensures agents don't advance until new temperature data is available.

## File Paths (SLURM Environment)

When running on the SLURM cluster, the code expects:
- EnergyPlus: `/project/lt200291-ignite/Project_chomwong/energyplus/EnergyPlus-25.1.0-*/`
- IDF file: `/project/lt200291-ignite/Project_chomwong/project/EnergyPlus_BP_Boonchoo/2ZoneDataCenterHVAC_wEconomizer.idf`
- Weather file: `/project/lt200291-ignite/Project_chomwong/project/EnergyPlus_BP_Boonchoo/DEU_BW_Stuttgart.AP.107380_TMYx.2009-2023.epw`

These are hardcoded in `main.py:65-66` and `model.py:46` - update for different environments.

## Agent Results Schema

The `agent_results` list (saved to CSV) contains per-agent, per-timestep records:
- `day`, `hour`, `step`: Time identifiers
- `agent_id`, `agent_type`: Agent identifiers
- `room`: Current zone location
- `current_temp`: Zone temperature experienced
- `comfort_level`: Calculated as `max(0, preferred_temp - abs(current_temp - preferred_temp))`
- `using_ac`: Boolean, whether agent wants cooling
- `preferred_temp`: Agent's temperature preference
