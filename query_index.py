from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

index = faiss.read_index("unspsc_index.faiss") # Load the index
model = SentenceTransformer("all-MiniLM-L6-v2") # Load the embedding model

# Query the index
def find_closest_unspsc(query: str, top_k=5):
    # Load code_name_pairs from pickle file
    with open("unspsc_lookup.pkl", "rb") as f:
        code_name_pairs = pickle.load(f)
    
    # Embed the query
    query_vector = model.encode([query], normalize_embeddings=True)
    query_vector = query_vector.astype('float32')

    # Search FAISS index
    D, I = index.search(np.array(query_vector), top_k)

    # # Print raw outputs
    # print("Similarity scores (D):", D)
    # print("Indices (I):", I)


    # Map results back to (code, name, score)
    results = []
    for rank, idx in enumerate(I[0]):
        code, name = code_name_pairs[idx]
        score = float(D[0][rank])
        results.append((code, name, score))
    return results


print(find_closest_unspsc("dog"))