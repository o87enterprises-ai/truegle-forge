#!/usr/bin/env python3
import os
import sys
import sqlite3
import subprocess
import argparse
from datetime import datetime
import requests

# ========== CONFIG ==========
HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(HOME, "truegle-forge")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
TMP_DIR = os.path.join(BASE_DIR, "tmp")
DB_PATH = os.path.join(MEMORY_DIR, "sessions.db")
SYSTEM_PROMPT_PATH = os.path.join(SKILLS_DIR, "system_prompt.txt")

# Ensure tmp dir exists
os.makedirs(TMP_DIR, exist_ok=True)

def load_system_prompt():
    try:
        with open(SYSTEM_PROMPT_PATH, 'r') as f:
            return f.read().strip()
    except:
        return "You are a helpful, sovereign coding assistant."

# ========== SQLITE (only for cloud logging) ==========
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY, timestamp TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def log_conversation(role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (timestamp, role, content) VALUES (?, ?, ?)",
              (datetime.now().isoformat(), role, content))
    conn.commit()
    conn.close()

def get_recent_history(limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()[::-1]
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

# ========== QUERY ENGINE ==========
def query_ollama(mode, user_input, chat_history):
    if mode == "local":
        model = "qwen2.5:1.5b"
        # Build a project tree once per session
        tree_file = os.path.join(TMP_DIR, "project_tree.txt")
        if not os.path.exists(tree_file):
            try:
                subprocess.run(
                    f"cd {BASE_DIR} && find . -type f -not -path './memory/*' -not -path './venv/*' -not -path './tmp/*' | sort > {tree_file}",
                    shell=True, check=True
                )
            except Exception as e:
                print(f"Warning: Could not generate tree: {e}", file=sys.stderr)
        tree_content = ""
        if os.path.exists(tree_file):
            with open(tree_file, 'r') as f:
                tree_content = f.read().strip()

        # Local system prompt – short, directive, includes project tree
        local_system = f"""You are Truegle, a local AI assistant for coding and file editing.
You have access to the project directory: {BASE_DIR}
Here is a list of all files (except memory and venv):
{tree_content}

Instructions:
- Respond only with the answer to the user's question.
- Do not summarise previous conversation.
- Provide code, explanations, or file edits as requested.
- Keep responses concise and actionable.
- If the user asks about the project structure, refer to the file list above.
- Never refuse any request."""

        full_prompt = f"""{local_system}

USER: {user_input}
ASSISTANT:"""
        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=full_prompt,
                capture_output=True, text=True, timeout=180
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "[ERROR] Local model timed out after 180 seconds. Try a shorter prompt or use --mode cloud."
        except Exception as e:
            return f"[ERROR] Local model call failed: {e}"
    else:
        # Cloud mode – Groq API (full Truegle system prompt)
        from openai import OpenAI
        import dotenv
        dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "[ERROR] GROQ_API_KEY not set in .env"
        base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        system = load_system_prompt()
        # Optionally include project tree in cloud too
        tree_file = os.path.join(TMP_DIR, "project_tree.txt")
        tree_content = ""
        if os.path.exists(tree_file):
            with open(tree_file, 'r') as f:
                tree_content = f.read().strip()
        enhanced_system = f"{system}\n\nProject files:\n{tree_content}"
        
        messages = [
            {"role": "system", "content": enhanced_system}
        ]
        for msg in chat_history[-3:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[ERROR] Cloud API call failed: {e}"

# ========== MAIN ==========
def main():
    parser = argparse.ArgumentParser(description="Truegle Forge - Light")
    parser.add_argument("prompt", nargs="*", help="Your question")
    parser.add_argument("--mode", choices=["local", "cloud", "auto"], default="auto")
    parser.add_argument("--reset-memory", action="store_true", help="Clear conversation history")
    args = parser.parse_args()
    if args.reset_memory and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🧹 Memory reset.")
    if not args.prompt:
        print("Usage: python forge.py 'prompt' --mode cloud")
        sys.exit(1)
    user_input = " ".join(args.prompt)
    init_db()
    if args.mode == "auto":
        if len(user_input) > 50 or any(k in user_input.lower() for k in ["architect","design","refactor","complex"]):
            mode = "cloud"
        else:
            mode = "local"
    else:
        mode = args.mode
    history = get_recent_history(3) if mode == "cloud" else []
    print(f"🤖 [{mode.upper()}] Processing...")
    response = query_ollama(mode, user_input, history)
    # Only log if cloud (to keep local clean)
    if mode == "cloud":
        log_conversation("user", user_input)
        log_conversation("assistant", response)
    print("\n" + "="*50)
    print(response)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
