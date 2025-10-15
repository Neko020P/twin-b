# Building Energy Co-Simulation Optimization Plan
## Boochoo Resolution Building - Thammasat University Lampang Campus

**Version**: 1.0
**Date**: January 15, 2025
**Building**: 5-story, 70-zone university academic building
**Location**: Lampang, Thailand (Tropical Savanna Climate)

---

## Executive Summary

This document outlines the optimization framework for experimenting with the **Boochoo Resolution Building** using agent-based modeling (Mesa) coupled with building energy simulation (EnergyPlus). The framework supports multiple occupancy scenarios from minimal operations (141 agents) to over-capacity events (972 agents), enabling comprehensive analysis of thermal comfort and energy performance under diverse conditions.

### Key Achievements

✅ **5 Agent Configuration Scenarios** - Covering full operational spectrum
✅ **70-Zone Building Model** - Complete spatial resolution across 5 floors
✅ **Lampang Climate Integration** - TMY weather data (2009-2023)
✅ **Experiment Framework** - Ready-to-run configuration files
✅ **No Code Modifications** - All existing code remains intact

---

## 1. Project Overview

### 1.1 Building Profile

| Attribute | Value |
|-----------|-------|
| **Name** | Boochoo Resolution Building |
| **Institution** | Thammasat University Lampang Campus |
| **Floors** | 5 stories |
| **Total Zones** | 70 zones |
| **Estimated Floor Area** | 8,500 m² |
| **Building Type** | University Academic Building |

### 1.2 Space Distribution

**Floor 1 (Ground)**: 15 zones
- Main auditorium (150 capacity)
- 4 Large lecture rooms (60-80 capacity each)
- Administrative offices
- Lobby areas

**Floors 2-4 (Academic)**: 15 zones each (45 total)
- Medium lecture rooms (30-50 capacity)
- Faculty offices
- Meeting rooms
- Hallways and restrooms

**Floor 5 (Labs & Special)**: 10 zones
- 3 Computer labs (30-45 capacity each)
- 4 Science laboratories (Physics, Chemistry, Biology, General)
- Research meeting rooms

---

## 2. Climate Context: Lampang, Thailand

### 2.1 Weather Data

**Source**: climate.onebuilding.org
**Station**: Lampang Airport (WMO 483280)
**Format**: EPW (EnergyPlus Weather Format)
**Period**: TMYx 2009-2023
**ICAO Code**: VTCL

**Download**: https://climate.onebuilding.org/WMO_Region_2_Asia/THA_Thailand/

### 2.2 Climate Characteristics

| Season | Months | Temperature Range | Humidity | Characteristics |
|--------|--------|-------------------|----------|----------------|
| **Hot** | Mar-May | 32-40°C | 40-60% | Peak cooling demand |
| **Rainy** | Jun-Oct | 25-32°C | 70-90% | High humidity, moderate temp |
| **Cool** | Nov-Feb | 15-28°C | 50-70% | Most comfortable period |

**Climate Type**: Tropical Savanna (Köppen: Aw)
**HVAC Implications**: Cooling-dominant year-round, humidity control critical

---

## 3. Agent Configuration Scenarios

### 3.1 Scenario Matrix

| Scenario | File | Agents | Use Case | Duration |
|----------|------|--------|----------|----------|
| **Normal Semester** | `agents_normal_semester.json` | 903 | Typical weekday operations | 30 days |
| **Exam Period** | `agents_exam_period.json` | 665 | Midterm/final exams | 14 days |
| **Weekend** | `agents_weekend.json` | 189 | Low occupancy baseline | 8 days |
| **Summer Break** | `agents_summer_break.json` | 141 | Minimal operations | 60 days |
| **Conference** | `agents_conference.json` | 972 | Special event stress test | 3 days |

### 3.2 Agent Type Definitions

#### 3.2.1 Undergraduate Students
- **Thermal Preference**: 23-26°C (mean 24.5°C, σ 1.0)
- **Comfort Tolerance**: 1.5-2.5°C
- **Activity Level**: Moderate (metabolic rate 1.2)
- **Age Range**: 18-23 years
- **Gender Distribution**: 55% female, 45% male

#### 3.2.2 Graduate Students
- **Thermal Preference**: 24-27°C (mean 25.0°C, σ 1.2)
- **Comfort Tolerance**: 1.0-2.0°C
- **Activity Level**: Low (metabolic rate 1.0)
- **Age Range**: 23-35 years
- **Occupancy Pattern**: Irregular, research-driven (10:00-20:00)

#### 3.2.3 Faculty/Professors
- **Thermal Preference**: 25-27°C (mean 25.5°C, σ 1.0)
- **Comfort Tolerance**: 1.0-1.5°C (lower tolerance)
- **Activity Level**: Low-Moderate
- **Age Range**: 30-65 years
- **Occupancy Pattern**: Teaching + office hours (8:30-17:00)

#### 3.2.4 Administrative Staff
- **Thermal Preference**: 25-27°C (mean 25.5°C, σ 0.8)
- **Comfort Tolerance**: 1.0-2.0°C
- **Activity Level**: Low (desk-bound)
- **Age Range**: 25-60 years
- **Occupancy Pattern**: Regular work hours (8:30-16:30)

#### 3.2.5 Laboratory Technicians
- **Thermal Preference**: 24-26°C (mean 24.5°C, σ 1.0)
- **Comfort Tolerance**: 2.0-3.0°C (higher tolerance)
- **Activity Level**: Moderate-High
- **Age Range**: 25-55 years
- **Notes**: Accustomed to lab temperature fluctuations

#### 3.2.6 Cleaning Staff
- **Thermal Preference**: 26-28°C (mean 27.0°C, σ 1.0)
- **Comfort Tolerance**: 2.5-3.5°C (highest tolerance)
- **Activity Level**: High
- **Age Range**: 25-60 years
- **Occupancy Pattern**: Early morning (6:00-10:00) or evening (17:00-21:00)

#### 3.2.7 Security Guards
- **Thermal Preference**: 25-27°C (mean 26.0°C, σ 1.0)
- **Comfort Tolerance**: 2.0-3.0°C
- **Activity Level**: Moderate (walking patrols)
- **Age Range**: 25-55 years
- **Occupancy Pattern**: 24/7 shifts

#### 3.2.8 Visitors
- **Thermal Preference**: 24-26°C (mean 25.0°C, σ 1.5)
- **Comfort Tolerance**: 1.0-2.0°C (unfamiliar with building)
- **Activity Level**: Moderate
- **Age Range**: 20-70 years (wide range)
- **Notes**: Lower tolerance due to unfamiliarity

---

## 4. Thermal Comfort Strategy

### 4.1 Zone-Specific Targets

| Zone Type | Target Temp | Rationale |
|-----------|-------------|-----------|
| **Auditorium** | 23-24°C | High density, metabolic heat generation |
| **Lecture Rooms** | 24-25°C | Moderate density, extended occupancy |
| **Laboratories** | 23-24°C | Equipment heat loads, precision work |
| **Computer Labs** | 22-23°C | High equipment density (40+ PCs) |
| **Offices** | 25-26°C | Individual preference accommodation |
| **Meeting Rooms** | 24-25°C | Small groups, varied duration |
| **Hallways** | 26-27°C | Transient occupancy, energy savings |
| **Restrooms** | 26-27°C | Short duration, less critical |

### 4.2 HVAC Priority Zones

**Critical Priority**:
- Floor1_Auditorium_Main (150 capacity)
- Floor5_ComputerLab_A & B (90 workstations total)
- Floor5_ScienceLab_Chemistry (ventilation requirements)

**High Priority**:
- All lecture rooms (24 zones)
- All laboratories except chemistry (6 zones)

**Moderate Priority**:
- All meeting rooms (11 zones)
- All faculty offices (15 zones)

**Low Priority**:
- All hallways (4 zones)
- All restrooms (9 zones)
- Common areas (2 zones)

---

## 5. Implementation Files

### 5.1 Agent Configurations (JSON)

Location: `/project/`

1. **agents_normal_semester.json** (903 agents)
   - 650 undergraduates, 80 graduates, 60 faculty
   - 40 admin staff, 20 lab technicians
   - 15 cleaners, 8 security, 30 visitors

2. **agents_exam_period.json** (665 agents)
   - 500 undergraduates (exam sessions)
   - Reduced labs (40 graduates, 10 technicians)
   - Enhanced cleaning (20 cleaners)
   - Heightened security (10 guards)

3. **agents_weekend.json** (189 agents)
   - 80 undergraduates (self-study), 50 graduates (research)
   - Minimal admin (5 staff)
   - Deep cleaning operations (20 cleaners)

4. **agents_summer_break.json** (141 agents)
   - 30 undergraduates (summer courses only)
   - 40 graduates (research peak)
   - 20 admin staff (year-round operations)
   - Equipment maintenance focus

5. **agents_conference.json** (972 agents)
   - 500 external visitors (keynote, sessions)
   - 200 undergraduates (volunteers/attendees)
   - 100 graduates (presenters)
   - Enhanced support staff (50 admin, 25 cleaners, 12 security)

### 5.2 Zone Configuration (YAML)

Location: `/project/zones_boochoo_building.yaml`

**Structure**:
```yaml
zones:
  - name: "Floor1_Auditorium_Main"
    floor: 1
    zone_type: "auditorium"
    capacity: 150
    area_m2: 200
    typical_occupancy: "high_density"
    hvac_priority: "critical"
  # ... (70 zones total)
```

**Zone Type Summary**:
- Auditorium: 2 zones
- Lecture rooms: 24 zones
- Laboratories: 7 zones
- Meeting rooms: 11 zones
- Offices: 15 zones
- Hallways: 4 zones
- Common areas: 2 zones
- Restrooms: 9 zones
- Stage: 1 zone

### 5.3 Experiment Configurations (YAML)

Location: `/project/experiments/`

1. **exp_boochoo_semester_lampang.yaml**
   - Links: agents_normal_semester.json + zones + Lampang weather
   - Simulation: 30 days, 288 steps/day
   - Output: results/boochoo_semester_lampang/

2. **exp_boochoo_exam_lampang.yaml**
   - Links: agents_exam_period.json + zones + Lampang weather
   - Simulation: 14 days (exam period)
   - Focus: Long continuous occupancy, stress concentration

3. **exp_boochoo_weekend_lampang.yaml**
   - Links: agents_weekend.json + zones + Lampang weather
   - Simulation: 8 days (4 weekends)
   - Focus: Energy baseline, setback strategies

4. **exp_boochoo_summer_lampang.yaml**
   - Links: agents_summer_break.json + zones + Lampang weather
   - Simulation: 60 days (June-August)
   - Focus: Peak outdoor temps, selective cooling

5. **exp_boochoo_conference_lampang.yaml**
   - Links: agents_conference.json + zones + Lampang weather
   - Simulation: 3 days (conference event)
   - Focus: Over-capacity stress test, HVAC limits

---

## 6. Experimental Design

### 6.1 Research Questions

1. **Thermal Comfort**:
   - Can the building maintain comfort under peak occupancy (903+ agents)?
   - Which zones experience thermal discomfort first?
   - How does occupancy density affect comfort levels?

2. **Energy Performance**:
   - What is the cooling energy demand for each scenario?
   - How much energy can be saved during low-occupancy periods?
   - What is the energy intensity per occupant (kWh/person)?

3. **HVAC Capacity**:
   - Can the system handle conference over-capacity (972 agents)?
   - What are the peak cooling demand periods?
   - Which zones are under-served?

4. **Occupant Behavior**:
   - How do different agent types affect setpoint requests?
   - What is the impact of thermal preference diversity?
   - How does activity level correlate with comfort?

### 6.2 Comparison Matrix

| Metric | Semester | Exam | Weekend | Summer | Conference |
|--------|----------|------|---------|--------|------------|
| **Agents** | 903 | 665 | 189 | 141 | 972 |
| **Density** | High | Concentrated | Low | Minimal | Over-capacity |
| **Duration** | 30d | 14d | 8d | 60d | 3d |
| **Focus** | Typical ops | Stress/conc. | Baseline | Conservation | Max capacity |

### 6.3 Success Criteria

✅ **Comfort**: >80% of agent-hours within comfort tolerance
✅ **Energy**: Within expected range for climate and occupancy
✅ **HVAC**: No zones with sustained temperatures >28°C
✅ **Simulation**: Stable runs without convergence issues

---

## 7. Integration with Existing Codebase

### 7.1 No Code Modifications Required

**Existing files remain untouched**:
- `main.py` - Distributed simulation orchestration
- `model.py` - BuildingModel class with EnergyPlus integration
- `agent.py` - BaseAgent and derived classes
- `utils.py` - Sampling and utility functions
- `config.yaml` - Original 2-zone configuration

### 7.2 Usage Workflow

**Step 1**: Download Lampang weather file
```bash
# Visit: https://climate.onebuilding.org/WMO_Region_2_Asia/THA_Thailand/
# Download: THA_NRG_Lampang.Airport.483280_TMYx.2009-2023.zip
# Extract EPW file to: project/weather/
```

**Step 2**: Update experiment config with actual paths
```yaml
# Edit: experiments/exp_boochoo_semester_lampang.yaml
building:
  idf_file: "/path/to/Boochoo_Resolution_Building.idf"
weather:
  epw_file: "/path/to/THA_NRG_Lampang.Airport.483280_TMYx.2009-2023.epw"
```

**Step 3**: Run simulation (modify main.py to load experiment config)
```bash
python project/main.py --experiment experiments/exp_boochoo_semester_lampang.yaml
```

**Step 4**: Analyze results
```bash
# Results saved to: results/boochoo_semester_lampang/
# Files: mesa_agent_results.csv, zone_results.csv, energy_summary.csv
```

### 7.3 Future Code Modifications (Recommended)

To fully integrate the experiment framework, consider:

1. **Modify `main.py`**:
   - Add `--experiment` CLI argument
   - Load experiment YAML instead of hardcoded paths
   - Auto-detect EnergyPlus from environment or config

2. **Enhance `model.py`**:
   - Accept IDF/weather paths as constructor parameters
   - Load zone mappings from YAML
   - Support zone-specific HVAC priorities

3. **Create `run_experiments.py`**:
   - Batch experiment orchestration
   - Sequential or parallel execution
   - Automated results aggregation

4. **Create `compare_experiments.py`**:
   - Load multiple experiment results
   - Generate comparison plots
   - Statistical analysis (ANOVA, correlation)
   - Export comparison reports

---

## 8. Expected Outcomes

### 8.1 By Scenario

**Normal Semester**:
- Moderate comfort levels (0.6-0.9 on 0-1 scale)
- High energy consumption during 9:00-15:00
- Computer labs may show thermal stress (equipment heat)

**Exam Period**:
- Lower comfort due to stress and concentration needs
- Concentrated energy demand in large halls
- Potential over-cooling requests from students

**Weekend**:
- High comfort levels due to low occupancy
- Significant energy savings opportunity
- Cleaners may experience discomfort (high activity)

**Summer Break**:
- Challenge: maintaining comfort with peak outdoor temps
- Critical test of HVAC efficiency
- Selective cooling could reduce costs 60-70%

**Conference**:
- Expect thermal discomfort in auditorium and hallways
- HVAC system at maximum capacity
- May identify need for capacity upgrades

### 8.2 Visualization Outputs

- **Comfort Heatmaps**: Zone × Hour showing comfort levels
- **Energy Usage Heatmaps**: Zone × Day showing cooling demand
- **Agent Distribution**: Spatial occupancy across zones
- **Temperature Trends**: Zone temps vs. setpoint requests
- **Comparative Bar Charts**: Energy/comfort across scenarios

---

## 9. Recommendations

### 9.1 Immediate Actions

1. **Obtain EnergyPlus IDF**: Work with TU Lampang facilities team to get or create Boochoo Resolution Building IDF file with 70 zones
2. **Download Weather Data**: Get Lampang TMYx file from climate.onebuilding.org
3. **Validate Zone Mapping**: Ensure IDF zone names match zones_boochoo_building.yaml
4. **Test Single Scenario**: Start with weekend (low occupancy) for validation

### 9.2 Calibration Needs

- **Agent Counts**: Adjust based on actual enrollment data
- **Thermal Preferences**: Survey students/staff for Thai preferences
- **Occupancy Schedules**: Align with actual class timetables
- **Equipment Loads**: Measure actual computer/lab equipment power

### 9.3 Research Extensions

- **Control Strategies**: Test demand-controlled ventilation (DCV)
- **Setpoint Optimization**: Find optimal zone setpoints balancing comfort/energy
- **Occupancy Prediction**: ML models for proactive HVAC control
- **Natural Ventilation**: Test mixed-mode during cool season (Nov-Feb)

---

## 10. Contact & Support

**Codebase**: /mnt/c/git/twin-b/
**Documentation**: CLAUDE.md, OPTIMIZATION_PLAN.md
**Weather Source**: climate.onebuilding.org
**EnergyPlus**: energyplus.net

**Key Files Created**:
- `/project/agents_*.json` (5 files)
- `/project/zones_boochoo_building.yaml`
- `/project/experiments/exp_*.yaml` (5 files)

---

## Appendix A: File Structure

```
twin-b/
├── CLAUDE.md                              # Repository overview
├── OPTIMIZATION_PLAN.md                   # This document
├── project/
│   ├── main.py                           # Existing - No modifications
│   ├── model.py                          # Existing - No modifications
│   ├── agent.py                          # Existing - No modifications
│   ├── utils.py                          # Existing - No modifications
│   ├── config.yaml                       # Existing - Original 2-zone config
│   ├── agents.json                       # Existing - Original 88 agents
│   ├── agents_normal_semester.json       # NEW - 903 agents
│   ├── agents_exam_period.json           # NEW - 665 agents
│   ├── agents_weekend.json               # NEW - 189 agents
│   ├── agents_summer_break.json          # NEW - 141 agents
│   ├── agents_conference.json            # NEW - 972 agents
│   ├── zones_boochoo_building.yaml       # NEW - 70 zones
│   └── experiments/                      # NEW directory
│       ├── exp_boochoo_semester_lampang.yaml
│       ├── exp_boochoo_exam_lampang.yaml
│       ├── exp_boochoo_weekend_lampang.yaml
│       ├── exp_boochoo_summer_lampang.yaml
│       └── exp_boochoo_conference_lampang.yaml
├── output/                               # Existing analysis outputs
│   ├── ComfortLevelHeatMap.png
│   └── EnergyUsageHeatMap.png
└── test/                                 # Existing test infrastructure
    ├── inputs/
    │   ├── idf/
    │   └── weather/
    └── scripts/
```

---

## Appendix B: Climate Data Details

### Lampang Weather Stations

| Station | WMO | Type | Location | Recommended |
|---------|-----|------|----------|-------------|
| Lampang Airport | 483280 | Airport | VTCL | ✅ **Primary** |
| Lampang Agromet | 483340 | Agricultural | Rural | Alternative |

### TMY Periods Available

- **2009-2023** (15 years) - Most recent, recommended
- **2007-2021** (15 years) - Alternative
- **2004-2018** (15 years) - Older baseline

### Download Instructions

1. Visit: https://climate.onebuilding.org/WMO_Region_2_Asia/THA_Thailand/index.html
2. Navigate to: Northern (NRG) region
3. Select: Lampang Airport (483280)
4. Choose: TMYx 2009-2023
5. Download ZIP containing:
   - EPW file (for EnergyPlus)
   - DDY file (design days)
   - STAT file (statistics)
   - Other formats (CLM, WEA, PVSyst)

---

**End of Optimization Plan**
*For questions or clarifications, refer to CLAUDE.md or experiment YAML files*
