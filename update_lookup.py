import pandas as pd
import numpy
import pickle

# Clean the dataset
df = pd.read_csv("unspsc_commodity_codes_and_names.csv", dtype={"unspsc_code": str})
records = df[["unspsc_code", "item_name"]].dropna(
).drop_duplicates().to_records(index=False)

# Create a python tuple (immutable) containing the index, name, and code of all UNSPSCs
code_name_pairs = list(records)
#print(len(code_name_pairs)) #QA -- Checks that code_name_pairs is not empty

# Store the code to item mapping
with open("unspsc_lookup.pkl", "wb") as f:
    pickle.dump(code_name_pairs, f)