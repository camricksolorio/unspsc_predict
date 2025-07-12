import faiss
import numpy

# Load the index
index = faiss.read_index("unspsc_index.faiss")

print("Number of vectors in index:", index.ntotal)