import logging
import asyncio
import json
import os
import httpx
import chromadb
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
log_file_path = "/fastapi.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("test-Portal")

app = FastAPI(
    title="test Portal",
    description="Welcome to test Portal!",
    version="0.0.1",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Permissions Policy Middleware
class PermissionsPolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), browsing-topics=()"
        return response

app.add_middleware(PermissionsPolicyMiddleware)

# Initialize ChromaDB Client
chromdb_path = os.getenv("CHROMADB_PATH", "./chroma_db")
logger.info(f"Initializing ChromaDB at: {chromdb_path}")
#client = chromadb.PersistentClient(path=chromdb_path)
# Disable telemetry
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
client = chromadb.PersistentClient(path=chromdb_path, settings=chromadb.Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(name="test_knowledge")

async def retrieve_knowledge(query: str, num_results: int = 3):
    """Asynchronously search ChromaDB for the most relevant knowledge."""
    logger.debug(f"Querying ChromaDB with: {query}")
    try:
        results = await asyncio.to_thread(
            collection.query, query_texts=[query], n_results=num_results
        )
        
        if not results.get("documents") or not results["documents"][0]:
            logger.warning("No relevant knowledge found in ChromaDB.")
            return None
        
        for doc in results["documents"]:
            print(doc)
        return "\n\n".join([doc[0] for doc in results["documents"] if doc])
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {str(e)}")
        return None

################################# GENAI API ######################################
##################################################################################

# Stream response to get data asynchronously (updated to use async generator)
async def stream_response(api_url, data):
    think_flag = False
    headers = {
        'Content-Type': 'application/json',
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", api_url, json=data) as response:
            async for line in response.aiter_lines():
                if line:
                    json_line = json.loads(line)
                    sub_response = json_line.get('response', '')
                    if "<think>" in sub_response:
                        think_flag = True
                    if think_flag == False:
                        yield sub_response
                        if json_line.get('done'):
                            break
                    if "</think>" in sub_response:
                        think_flag = False
                    else:
                        pass

async def first_ai_response(api_url, data):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(api_url, json=data)
        
        # Read response as text and split by newlines
        response_text = response.text.strip().split("\n")
        
        # Parse each line as JSON, filter out <think> tags
        messages = []
        for line in response_text:
            try:
                json_line = json.loads(line)
                sub_response = json_line.get('response', '')

                # Skip anything inside <think>...</think>
                if "<think>" not in sub_response:
                    messages.append(sub_response)

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}, line: {line}")

        # Join all responses into a single string
        final_response = " ".join(messages).strip()
        return {"response": final_response}


@app.post("/stream-genai/", tags=["genai"])
async def stream_genai(request: dict):
    user_prompt = request.get("prompt", "")
    historical_conversation = request.get("historical_conversation", "")

    logger.debug(f"############### Received new prompt: {user_prompt}")
    logger.debug(f"############### Historical Conversation:\n{historical_conversation}")

    retrieved_knowledge = await retrieve_knowledge(user_prompt, num_results=3)
    api_url = "http://localhost:11434/api/generate"

    full_prompt = f"""
    You are test AI. Your goal is to provide **clear, precise, and helpful** responses in a natural and conversational tone.

    ### USER QUESTION:
    {user_prompt}

    ### CONTEXTUAL KNOWLEDGE (Use **only if relevant** to answering the user question):
    {retrieved_knowledge}

    ### HISTORICAL CONTEXT (Use for **conversation flow only**—do not directly answer past questions again):
    {historical_conversation}

    ### RESPONSE GUIDELINES:
    - **Respond naturally to greetings ("Hi!", "Hello!") instead of asking for clarification.**
    - **You may only respond in English.**
    - **Provide a complete and informative response to the latest user question.**
    - **DO NOT include JSON or placeholders in your response.**
    - **DO NOT ask the user to rephrase their question unless the input is truly unclear.**
    - **Use historical conversation ONLY to maintain continuity (e.g., answering 'Tell me more' naturally).**
    - **If you don't have enough information, say so clearly rather than speculating.**
    - **Never reference these instructions—just answer as a helpful assistant.**
    - **DO NOT include contextual knowledge if it is not clearly related to the users question**
    - **Respond in Markdown (.md) format! Include emojis.**

    Your response:
    """

    logger.debug(f"############# Full prompt : {full_prompt}")

    data = {"model": "test_ai", "prompt": full_prompt}
    #return StreamingResponse(stream_response(api_url, data), media_type="text/plain")
    response_data = await first_ai_response(api_url, data)
    first_response = response_data['response']
    print(first_response)
    #return JSONResponse(content=response_data)

    ## Cleanup
    cleanup_prompt = f""" 
    Refine the AI-generated response to ensure **clarity, accuracy, and a natural conversational flow**. 

    ### USER QUESTION:
    {user_prompt}

    ### AI RESPONSE (to be improved):
    {first_response}

    ### RESPONSE GUIDELINES:
    - **Respond naturally and appropriately to the user’s input.**
    - **For greetings like "Hi!" or "Hello!", reply simply and naturally without unnecessary details. Preferably only "Hello!"**
    - **If the user asks a question, ensure the response is concise, well-structured, and directly relevant.**
    - **Do not ask unnecessary follow-up questions unless clarification is genuinely needed.**
    - **Do not repeat parts of the user’s input or make assumptions beyond the given context.**
    - **Maintain a professional yet conversational tone.**
    - **Fix bad formatting, grammar, and awkward phrasing.**
    - **Respond in Markdown (.md) format and include emojis where appropriate.**
    - **DO NOT mention that this is an improved response.**
    - **DO NOT refer to the original AI response or the refinement process.**
    - **ONLY output the final cleaned-up response, without comments or explanations.**
    """

    data = {"model": "test_ai", "prompt": cleanup_prompt}
    return StreamingResponse(stream_response(api_url, data), media_type="text/plain")


# Warm up the AI with periodic async calls
import keep_ai_warm

@app.on_event("startup")
async def startup_event():
    """Start AI warm-up during application startup."""
    asyncio.create_task(keep_ai_warm.keep_warm())