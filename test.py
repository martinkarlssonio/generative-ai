import requests
import json
import sys

API_URL = "http://{ENDPOINT}:8010/stream-genai/"

def test_streaming_api(prompt):
    """
    Sends a request to the streaming API and prints the response character by character.
    Ensures real-time, seamless output while handling encoding errors gracefully.
    """
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"prompt": prompt})

    with requests.post(API_URL, data=data, headers=headers, stream=True) as response:
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return

        print("\nStreaming Response:\n" + "-"*40)

        full_response = ""
        for chunk in response.iter_content(chunk_size=1):  # Stream character-by-character
            if chunk:
                try:
                    char = chunk.decode("utf-8", errors="ignore")  # Ignore decoding errors
                    sys.stdout.write(char)  # Print immediately
                    sys.stdout.flush()  # Ensure real-time output
                    full_response += char
                except UnicodeDecodeError:
                    continue  # Skip problematic bytes

        print("\n\nFull Response:\n" + "-"*40)
        print(full_response)

if __name__ == "__main__":
    user_prompt = input("Enter your test prompt: ")
    test_streaming_api(user_prompt)