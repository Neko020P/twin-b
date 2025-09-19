# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import pandas as pd
from agents import StudentAgent, StaffAgent, CleanerAgent, WardenAgent, VisitorAgent

class BuildingModel(Model):
    def __init__(self, config):
        self.schedule = RandomActivation(self)
        self.config = config
        self.current_step = 0

        self.energy_data = pd.read_csv(config["energyplus"]["csv_file"])
        self.agent_results = []

        agent_types = {
            "students": StudentAgent,
            "staff": StaffAgent,
            "cleaners": CleanerAgent,
            "wardens": WardenAgent,
            "visitors": VisitorAgent
        }

        uid_list = config.get("mesa", {}).get("agent_ids", None)
        if uid_list is not None:
            # สำหรับ distributed simulation: สร้าง agent ตาม uid partition ของ rank
            idx = 0
            for atype, cls in agent_types.items():
                n_agents = config["mesa"]["agents"].get(atype, 0)
                for _ in range(n_agents):
                    if idx < len(uid_list):
                        agent = cls(uid_list[idx], self)
                        self.schedule.add(agent)
                        idx += 1
        else:
            # fallback: สร้างทุก agent
            uid = 0
            for atype, cls in agent_types.items():
                for _ in range(config["mesa"]["agents"].get(atype, 0)):
                    agent = cls(uid, self)
                    self.schedule.add(agent)
                    uid += 1

        self.datacollector = DataCollector(
            model_reporters={
                "AvgTemp_West": lambda m: m.get_current_temp("West Zone"),
                "AvgTemp_East": lambda m: m.get_current_temp("East Zone")
            }
        )

    def get_current_temp(self, zone_name):
        if self.current_step < len(self.energy_data):
            if zone_name == "West Zone":
                return self.energy_data.iloc[self.current_step, 1]
            elif zone_name == "East Zone":
                return self.energy_data.iloc[self.current_step, 2]
        return None

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.current_step += 1
