import pandas as pd

csv_file = "/project/lt200291-ignite/Project_chomwong/test/runs/run7/2ZoneDataCenterHVAC_wEconomizer.csv"

df = pd.read_csv(csv_file)

print(df.columns)

cols = ["Date/Time",
        "WEST ZONE:Zone Air Temperature [C](TimeStep)",
        "EAST ZONE:Zone Air Temperature [C](TimeStep)"]

df_selected = df[cols]

output_file = "/project/lt200291-ignite/Project_chomwong/test/runs/run7/2Zone_ZoneAirTemp.csv"
df_selected.to_csv(output_file, index=False)

print(f"✅ Saved filtered CSV to {output_file}")
