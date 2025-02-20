import os
import json
import sys
from knowledge_manager import add_knowledge

# Use environment variable if set, otherwise default to "jsonl"
jsonl_folder = os.getenv("JSONL_FOLDER", "jsonl")

def count_total_lines(folder):
    """Counts the total number of lines across all JSONL files."""
    total_lines = 0
    for jsonl_filename in os.listdir(folder):
        if jsonl_filename.endswith(".jsonl"):
            jsonl_path = os.path.join(folder, jsonl_filename)
            with open(jsonl_path, "r", encoding="utf-8") as f:
                total_lines += sum(1 for _ in f)
    return total_lines

def populate_chromadb():
    """Populates ChromaDB with knowledge from all JSONL files while showing a live percentage counter."""
    
    total_lines = count_total_lines(jsonl_folder)
    processed_lines = 0  

    if total_lines == 0:
        print("\r⚠ No JSONL files found or they are empty.", end="", flush=True)
        return

    for jsonl_filename in os.listdir(jsonl_folder):
        if jsonl_filename.endswith(".jsonl"):
            jsonl_path = os.path.join(jsonl_folder, jsonl_filename)

            try:
                with open(jsonl_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            query = entry.get("instruction", "").strip()
                            answer = entry.get("output", "").strip()

                            if query and answer:
                                add_knowledge(query, answer)
                                processed_lines += 1

                                # Update the same line with percentage progress
                                progress_percent = (processed_lines / total_lines) * 100
                                sys.stdout.write(f"\r{progress_percent:.2f}% Complete")
                                sys.stdout.flush()

                        except json.JSONDecodeError:
                            continue  # Skip invalid JSON lines

            except Exception:
                continue  # Skip any file errors

    sys.stdout.write("\r100.00% Complete\n")  # Final update for cleanliness

# Run the population script
populate_chromadb()
