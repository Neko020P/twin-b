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

        # โหลด EnergyPlus CSV
        self.energy_data = pd.read_csv(config["energyplus"]["csv_file"])

        # สร้าง list เก็บผลลัพธ์ agent
        self.agent_results = []

        # สร้าง agent
        agent_types = {
            "students": StudentAgent,
            "staff": StaffAgent,
            "cleaners": CleanerAgent,
            "wardens": WardenAgent,
            "visitors": VisitorAgent
        }

        uid = 0
        for atype, cls in agent_types.items():
            for _ in range(config["mesa"]["agents"][atype]):
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
            # สมมติ column 1=West Zone, 2=East Zone
            if zone_name == "West Zone":
                return self.energy_data.iloc[self.current_step, 1]
            elif zone_name == "East Zone":
                return self.energy_data.iloc[self.current_step, 2]
        return None

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.current_step += 1
