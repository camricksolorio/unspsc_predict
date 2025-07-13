# # 1) Ensure that the csv contents are as expected
# import pandas as pd
# df = pd.read_csv("unspsc_commodity_codes_and_names.csv", dtype={"unspsc_code": str})
# records = df[["unspsc_code", "item_name"]].dropna(
# ).drop_duplicates().to_records(index=False)

# first_five_rows = df.head()
# first_five_rows_explicit = df.head(5) # To explicitly specify 5 rows
# print(first_five_rows)

###

# # 2) Ensure that unslsc_lookup.pkl contains UNSPSC codes and names in the expected format
# import pickle
# with open("unspsc_lookup.pkl", "rb") as f:
#     data = pickle.load(f)
# for row in data[:5]:
#     print(row)

###

# # 3) Ensure the unspsc_index returned by faiss has the expected number of vectors
# import faiss
# import numpy
# index = faiss.read_index("unspsc_index.faiss")
# print("Number of vectors in index:", index.ntotal)