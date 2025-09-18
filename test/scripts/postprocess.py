import argparse
import pandas as pd
import os

def eso_to_csv(eso_file, out_file):
    if not os.path.exists(eso_file):
        raise FileNotFoundError(f"❌ ไม่พบไฟล์ {eso_file}")

    data = []
    in_data = False

    with open(eso_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.lower() == "end of data dictionary":
                in_data = True
                continue
            if in_data:
                parts = line.split(",")
                row = []
                for p in parts:
                    try:
                        row.append(float(p))
                    except ValueError:
                        row.append(p.strip())
                data.append(row)

    headers = ["col1","col2","col3","col4","col5","col6","col7","col8","col9"]
    df = pd.DataFrame(data, columns=headers)

    df.to_csv(out_file, index=False)
    print(f"✅ Exported {out_file} with {len(df)} rows")
    return df

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--eso", required=True, help="/project/lt200291-ignite/Project_chomwong/test/runs/run7/run7out.eso")

    parser.add_argument("--out", required=True, help="/project/lt200291-ignite/Project_chomwong/test/runs/run7/run7_temperature.csv")

    args = parser.parse_args()
 
    eso_to_csv(args.eso, args.out)

 
