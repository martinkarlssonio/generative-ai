# Use Debian-based Python image (better compatibility with onnxruntime
FROM nvcr.io/nvidia/tensorflow:23.12-tf2-py3

# Set non-interactive mode to prevent tzdata from asking input
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /

# Copy application files
COPY ai /ai
COPY fastapi /fastapi
COPY start.sh /start.sh
COPY requirements.txt /

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    nodejs \
    npm \
    git \
    gcc \
    g++ \
    make \
    musl-dev \
    python3-dev \
    libffi-dev \
    unzip \
    cmake \
    bash \
    curl \
    ca-certificates \
    binutils \
    numactl \
    build-essential \
    libstdc++6 \
    libssl-dev \
    libopenblas-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Install OpenJDK 21 from Adoptium (Eclipse Temurin)
RUN curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /usr/share/keyrings/adoptium.asc && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb bookworm main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends temurin-21-jdk && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python pip is upgraded
RUN pip install --no-cache-dir --upgrade pip

# Manually install onnxruntime first (required by ChromaDB)
RUN pip install --no-cache-dir onnxruntime==1.14.1

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

### AI Setup #####################################################################

## Populate ChromaDB Knowledge Base
# Knowledge path
ENV JSONL_FOLDER=/ai/knowledge/jsonl
ENV CHROMADB_PATH=/ai/knowledge/chroma_db
WORKDIR /ai/knowledge/
RUN python populate_knowledge.py
WORKDIR /

# Install Golang (latest version for Ollama)
ARG GOLANG_VERSION=1.21.0
RUN curl -LO "https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz" && \
    tar -C /usr/local -xzf "go${GOLANG_VERSION}.linux-amd64.tar.gz" && \
    rm "go${GOLANG_VERSION}.linux-amd64.tar.gz"
ENV PATH=$PATH:/usr/local/go/bin

# Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set Ollama host
ENV OLLAMA_HOST=0.0.0.0:11434

# Return to root directory
WORKDIR /

# Ensure AI build script is executable and run it
RUN chmod +x /ai/build_script.sh
RUN sh /ai/build_script.sh

# Expose necessary ports
EXPOSE 8010
EXPOSE 8050

# Ensure start script is executable
RUN chmod +x /start.sh


# Start the application
CMD ["/start.sh"]
