import geopandas as gpd
import pandas as pd
from unidecode import unidecode
import re

cases = pd.read_excel("cases_new.xlsx").dropna()
data = gpd.read_file("concelhos_david (1).geojson")

f = lambda x: unidecode(re.sub(r"\d", "", x.lower()).strip())
cases["ProvinceName"] = cases["ProvinceName"].apply(f)
data["NAME_2"] = data["NAME_2"].apply(f)

# Group by by name
grouped_cases = cases.groupby("ProvinceName").agg({"24/Mar": "mean", "Number of Infected":"sum"})


# Merge data
merged = data.merge(grouped_cases, right_index=True, left_on="NAME_2", how="inner")
merged.rename(columns={"24/Mar": "Risk"}, inplace=True)
merged.to_file("countries.geojson", driver='GeoJSON')
