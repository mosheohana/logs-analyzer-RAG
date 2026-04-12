"""
RAG over log data

This script loads parsed log data, converts each row into a textual chunk,
embeds the chunks, retrieves the most relevant ones for a query, and
prints retrieved evidence along with a generated natural-language answer.
"""

import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

# -------- 1) load parsed logs --------
df = pd.read_csv("parsed_logs.csv")

# text representation per row
def row_to_text(row):
    return (
        f"At {row['time']} IP {row['ip']} "
        f"sent {row['method']} request to {row['path']} "
        f"and server returned status {row['status']}."
    )

documents = df.apply(row_to_text, axis=1).tolist()

# -------- 2) embed documents --------
model = SentenceTransformer("all-MiniLM-L6-v2")

doc_embeddings = model.encode(documents, convert_to_numpy=True)

# build FAISS index
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(doc_embeddings)

print(f"Indexed {len(documents)} log entries.")


# -------- 3) interactive query loop --------
def ask(query, k=5):
    query_emb = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k)

    print("\nRetrieved relevant log lines:")
    for i in indices[0]:
        print("-", documents[i])

    # very simple "generation"
    print("\nAnswer (summary style):")
    print(f"The query '{query}' is related to the retrieved events above.")
    print("You can inspect IPs, status codes, and timestamps for investigation.")


# -------- 4) example questions --------
if __name__ == "__main__":

    print("\nExample queries you can try:")
    print("- failed login attempts")
    print("- suspicious IP activity")
    print("- many requests from same IP")
    print("- 404 errors")
    print("- brute-force attack")

    while True:
        q = input("\nType your question (or 'exit'): ")
        if q.lower() == "exit":
            break
        ask(q)
