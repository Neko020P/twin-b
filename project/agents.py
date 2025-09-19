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

