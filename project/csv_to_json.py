# csv_to_json.py
import argparse
import pandas as pd
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--csv", type=str, required=True, help="Path to CSV file")
parser.add_argument("--json", type=str, required=True, help="Path to output JSON file")
args = parser.parse_args()

# อ่าน CSV
df = pd.read_csv(args.csv)

# สร้างโฟลเดอร์ output ถ้ายังไม่มี
os.makedirs(os.path.dirname(args.json), exist_ok=True)

# บันทึกเป็น JSON
df.to_json(args.json, orient="records", indent=2)

print(f"[OK] Saved JSON -> {args.json}")

