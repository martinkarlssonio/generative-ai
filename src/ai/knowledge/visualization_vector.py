import chromadb
from sklearn.decomposition import PCA
import plotly.express as px
from dash import Dash, dcc, html

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path="./chroma_db")

# Load the collection
collection = client.get_collection(name="test_knowledge")

# Get embeddings and metadata
data = collection.get(include=['embeddings', 'documents', 'metadatas'])
embeddings = data.get('embeddings', [])
documents = data.get('documents', [])
metadatas = data.get('metadatas', [])

# Ensure embeddings exist
if embeddings is None or len(embeddings) == 0:
    raise ValueError("No embeddings found in the database. Add data first!")

# Extract meaningful labels (shortened version of the documents)
labels = []
for doc, meta in zip(documents, metadatas):
    if isinstance(doc, list):  # Handle nested structure
        doc = doc[0]
    summary = doc[:80] + "..." if len(doc) > 80 else doc  # Truncate for readability
    instruction = meta.get("instruction", "") if meta else ""
    labels.append(f"{instruction[:60]}...")  # Show part of the instruction

# Reduce dimensionality for visualization
pca = PCA(n_components=3)
vis_dims = pca.fit_transform(embeddings)

# Create an interactive 3D plot
fig = px.scatter_3d(
    x=vis_dims[:, 0],
    y=vis_dims[:, 1],
    z=vis_dims[:, 2],
    text=labels,
    labels={
        'x': 'Topic Similarity',
        'y': 'Contextual Difference',
        'z': 'Concept Grouping'
    },
    title='3D Knowledge Embedding Visualization'
)

# Set up Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Knowledge Embedding Visualization"),
    dcc.Graph(figure=fig, style={"height": "90vh"})
])

# Run the Dash app on 0.0.0.0 to make it accessible from other devices
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
