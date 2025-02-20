import chromadb
import uuid

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load a collection
collection = client.get_or_create_collection(name="test_knowledge")

def retrieve_knowledge(query):
    """Search ChromaDB for the most relevant knowledge."""
    results = collection.query(
        query_texts=[query],
        n_results=1  # Fetch only the most relevant match
    )

    if not results["documents"] or not results["documents"][0]:
        return "NO_KNOWLEDGE_FOUND"
    print(results)
    print(results['documents'])
    return results["documents"][0][0]  # Extract first result properly

def add_knowledge(query, answer):
    """Add new knowledge to ChromaDB while ensuring unique IDs."""
    unique_id = str(uuid.uuid4())  # Generate a unique ID for each entry

    try:
        collection.add(
            ids=[unique_id],
            documents=[answer],
            metadatas=[{"instruction": query}]
        )
        print(f"✔ Knowledge successfully added: {query}")
    except Exception as e:
        print(f"❌ Error adding knowledge: {e}")

if __name__ == "__main__":
    print("✔ ChromaDB setup complete.")
