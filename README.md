# **GenAI Container with Custom Knowledge Retrieval (RAG)**

This repository contains a **Generative AI container** designed to interact with a **vector database** (ChromaDB) to enhance responses using **Retrieval-Augmented Generation (RAG)**. The system indexes domain-specific knowledge and retrieves relevant embeddings to provide accurate and context-aware responses.

## **Features**
- **Custom Knowledge Base**: Stores and retrieves structured knowledge using ChromaDB.
- **Vector Database Integration**: Efficient similarity search for response augmentation.
- **FastAPI API**: Provides a RESTful interface for AI-powered queries.
- **Ollama-based GenAI**: Runs AI models locally to generate responses.
- **GPU-Accelerated**: Optimized for NVIDIA GPUs with TensorFlow.
- **Interactive Visualization**: Embedding inspection using Dash and Plotly.

---

## **Repository Structure**
```
GEN-AI/
│── src/
│   ├── ai/
│   │   ├── knowledge/
│   │   │   ├── json/
│   │   │   ├── mocked_data.jsonl  # Sample knowledge data
│   │   │   ├── knowledge_manager.py  # Handles knowledge ingestion
│   │   │   ├── populate_knowledge.py  # Populates ChromaDB with knowledge
│   │   │   ├── visualization_vector.py  # 3D embedding visualization
│   │   │   ├── build_script.sh  # AI model setup script
│   │   ├── Modelfile  # Model configuration
│   │   ├── requirements.txt
│   ├── fastapi/app/
│   │   ├── main.py  # FastAPI backend for AI responses
│   │   ├── models.py  # AI model handling
│   │   ├── keep_ai_warm.py  # Keeps AI ready for requests
│   │   ├── build_push_image.sh  # Docker build and push script
│── Dockerfile  # Container definition
│── start.sh  # Container startup script
│── requirements.txt
│── README.md
│── test.py  # Unit tests
│── .gitignore
```

---

## **Setup & Installation**
### **1. Clone the Repository**
```bash
git clone <repository-url>
cd generative-ai
```

### **2. Build & Run the Container**
#### **Build the Docker Image**
```bash
docker build -t genai-container .
```

#### **Run the Container**
```bash
docker run --rm -p 8010:8010 -p 8050:8050 genai-container
```
- The **FastAPI server** will be available at `http://localhost:8010`
- The **Vector Embedding Visualization** will be at `http://localhost:8050`

### **3. Install Dependencies for Local Development**
```bash
pip install -r requirements.txt
```

---

### **Query the AI API**
#### **Streamed AI Response with RAG**
```bash
curl -X POST "http://localhost:8010/stream-genai/" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "How do industrial robots benefit from vector databases?"}'
```
Example JSON Response:
```json
{
  "response": "Industrial robots benefit from vector databases by enabling fast similarity searches on motion data, improving predictive maintenance, and optimizing navigation paths."
}
```

---

## **Key Components**
### **1. Vector Database (ChromaDB)**
- Stores embeddings of structured knowledge for fast retrieval.
- Supports **similarity search** to augment AI responses.

### **2. FastAPI Backend**
- Handles AI inference requests.
- Integrates with ChromaDB for knowledge retrieval.
- Implements **streamed responses** for real-time interaction.

### **3. AI Model (Ollama)**
- Uses local **LLM models** to generate intelligent responses.
- Embeds **retrieved knowledge** into answers dynamically.

### **4. Visualization (Dash + Plotly)**
- Provides a **3D visualization of knowledge embeddings**.
- Helps in **debugging** vector similarity and clustering.

---

## **Development & Debugging**
### **Check Running Containers**
```bash
docker ps
```

### **Attach to Running Container**
```bash
docker exec -it <container-id> /bin/bash
```

### **Test API Locally**
```bash
pytest test.py
```

---

## **Deployment**
### **Build & Push to AWS ECR (Container Image Registry)**
```bash
./src/fastapi/app/build_push_image.sh
```

### **Run Locally with GPU (ensure you have a supported GPU and enough resources to run it locally)**
```bash
docker run --gpus all -p 8010:8010 -p 8050:8050 genai-container
```