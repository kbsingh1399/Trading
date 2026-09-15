import os
import pandas as pd
data_dir = "Forex_Backtesting_Data"
files = [f for f in os.listdir(data_dir) if "15m" in f]
earliest_dates = []
for f in files:
    df = pd.read_parquet(os.path.join(data_dir, f))
    earliest_dates.append(df['time'].min())

print("Min date across all assets:", min(earliest_dates))
print("Max earliest date across assets:", max(earliest_dates))
earliest_dates.sort()
print("75th percentile earliest date:", earliest_dates[int(len(earliest_dates)*0.75)])
