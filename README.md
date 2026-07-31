\# 🔥 Truegle Forge – Sovereign AI Assistant



\*\*Truegle Forge\*\* is a sovereign, uncensored AI coding assistant that runs locally (via Ollama) or in the cloud (via Groq API). It features a powerful CLI harness and a branded web UI, designed for maximum autonomy and user control.



> 🚀 \*\*Live Demo\*\* – \[https://truegle-forge.onrender.com](https://truegle-forge.onrender.com)



\---



\## ✨ Features



\- \*\*Uncensored \& sovereign\*\* – No safety filters, pure user‑driven responses.

\- \*\*Dual mode\*\* – Local (Ollama) for offline use, or Cloud (Groq) for speed.

\- \*\*CLI\*\* – Quick terminal access for scripting and automation.

\- \*\*Web UI\*\* – Branded dark‑themed interface with conversation history.

\- \*\*Cross‑platform\*\* – Works on Windows, Linux, macOS, and even Android (Termux).



\---



\## 🧰 Prerequisites



\- \*\*Python 3.10+\*\* – \[Download](https://python.org/downloads)

\- \*\*Groq API key\*\* (for cloud mode) – \[Get one here](https://console.groq.com)

\- \*\*Ollama\*\* (for local mode) – \[Install Ollama](https://ollama.com)



\---



\## 📦 Installation (All Platforms)



1\. \*\*Clone the repository:\*\*

&#x20;  ```bash

&#x20;  git clone https://github.com/o87enterprises-ai/truegle-forge.git

&#x20;  cd truegle-forge


    Create a virtual environment (optional but recommended):
    bash

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    .\venv\Scripts\activate    # Windows

    Install dependencies:
    bash

    pip install -r web/requirements.txt

    Set up your Groq API key (for cloud mode):
    Create a .env file in the project root with:
    text

    GROQ_API_KEY=your_api_key_here
    GROQ_MODEL=llama-3.3-70b-versatile
    GROQ_BASE_URL=https://api.groq.com/openai/v1

🖥️ CLI Usage (Desktop & Termux)
Cloud Mode (Groq)
bash

python harness/forge.py "What is your purpose?" --mode cloud

Local Mode (Ollama)
bash

python harness/forge.py "List all files" --mode local

Reset Memory (Cloud mode only)
bash

python harness/forge.py --reset-memory

📱 Termux (Android) Setup

    Install Termux from F‑Droid (not Play Store).

    Update and install Python:
    bash

    pkg update && pkg upgrade
    pkg install python git

    Clone and install as above (use pip without virtual environment if preferred).

    Run CLI commands the same way.

🌐 Web UI (Graphical Interface)

    Ensure .env is set with your Groq API key.

    Run the Flask server:
    bash

    python web/app.py

    Open your browser to http://127.0.0.1:5000

    Start chatting – the UI uses the same sovereign prompt.


Deploy to Production

    Render (recommended): Push your repo to GitHub and create a Web Service with Python environment – guide.

    Vercel: Supports Flask via Serverless Functions – guide.

🎨 Branding

The web UI uses your own Truegle logo (placed in web/static/logo.png) and a dark theme with the tagline "Unbiased · Transparent · Secure". The system prompt is fully customisable in skills/system_prompt.txt.
📂 Project Structure
text

truegle-forge/
├── .env                      # Groq API key (excluded from Git)
├── harness/
│   └── forge.py              # CLI harness (local/cloud)
├── skills/
│   └── system_prompt.txt     # The Truegle system prompt
├── web/
│   ├── app.py                # Flask backend
│   ├── requirements.txt      # Python dependencies
│   ├── static/
│   │   └── logo.png          # Your brand logo
│   └── templates/
│       └── index.html        # Branded dark UI
├── memory/                   # SQLite logs (cloud mode)
└── README.md                 # This file

🛠️ Customisation

    System prompt: Edit skills/system_prompt.txt to change the AI's personality and rules.

    Logo: Replace web/static/logo.png with your own image (PNG, ~44px height recommended).

    Theme: Edit web/templates/index.html CSS to adjust colours and layout.

🤝 Contributing

We welcome contributions! Fork the repo, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.
📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
🙏 Acknowledgements

    Groq for the fast cloud inference.

    Ollama for local model serving.

    Flask for the web framework.

Truegle Forge – built with ❤️ by the Truegle team.

