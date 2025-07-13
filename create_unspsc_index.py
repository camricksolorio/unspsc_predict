import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Clean the dataset
df = pd.read_csv("unspsc_commodity_codes_and_names.csv", dtype={"unspsc_code": str})  # or Excel, SQL, etc.
records = df[["unspsc_code", "item_name"]].dropna(
).drop_duplicates().to_records(index=False)

# Create a python tuple (immutable) containing the index, name, and code of all UNSPSCs
code_name_pairs = list(records)
#print(len(code_name_pairs)) #QA -- Checks that code_name_pairs is not empty

# Create an array of JUST the UNSPSC cnames
item_names = [name for _, name in code_name_pairs] 
# print(len(item_names)) ##QA -- Checks that item_names is not empty


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate normalized embeddings
embeddings = model.encode(item_names, normalize_embeddings=True)
embeddings = embeddings.astype('float32') # Ensure embeddings are float32


# Determine vector dimension
embedding_dim = embeddings.shape[1]  # (e.g. 151000, 354)

# Create FAISS index for cosine similarity (using inner product)
index = faiss.IndexFlatIP(embedding_dim)

# Add embeddings to index
index.add(embeddings)

# Store the index
faiss.write_index(index, "unspsc_`index.faiss")

# Store the code to item mapping
with open("unspsc_lookup.pkl", "wb") as f:
    pickle.dump(code_name_pairs, f)