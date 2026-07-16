import pandas as pd

df = pd.read_csv("data/battery_log.csv")

print(df["Charging_Status"].unique())
