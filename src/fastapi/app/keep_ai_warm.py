import asyncio
import httpx
import json
import logging

logger = logging.getLogger("test-Portal-KeepWarm")

async def stream_response(api_url, data, retries=3):
    headers = {'Content-Type': 'application/json'}
    timeout = httpx.Timeout(30.0, connect=5.0)
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream("POST", api_url, json=data) as response:
                    async for line in response.aiter_lines():
                        if line:
                            json_line = json.loads(line)
                            #sub_response = json_line.get('response', '')
                            #logger.info(f"Keep Warm Response: {sub_response}")
                            if json_line.get('done'):
                                return
        except httpx.RequestError as exc:
            logger.warning(f"Attempt {attempt+1} failed: {exc}")
            if attempt + 1 == retries:
                logger.error(f"Failed after {retries} retries.")
                break
        await asyncio.sleep(2)

async def keep_warm():
    """Keep the AI warm by sending periodic requests."""
    while True:
        api_url = "http://localhost:11434/api/generate"
        data = {
            "model": "test_ai",
            "prompt": "Only respond with: OK, thank you!"
        }
        await stream_response(api_url, data)
        logger.info("AI now warm and ready!")
        await asyncio.sleep(60)
