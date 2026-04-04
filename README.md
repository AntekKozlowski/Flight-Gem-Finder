# ✈️ Flight Gem Finder (Multi-Agent AI System)

![Status](https://img.shields.io/badge/Status-Stable-green)
![Language](https://img.shields.io/badge/language-Python_3.11-blue)
![Architecture](https://img.shields.io/badge/architecture-Multi--Agent-orange)
![Database](https://img.shields.io/badge/database-SQLite-lightgrey)
![Container](https://img.shields.io/badge/platform-Docker-blue)
![Testing](https://img.shields.io/badge/testing-Pytest-yellowgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Flight Gem Finder is an autonomous, high-performance Multi-Agent AI System designed to act as a personal travel analyst. It features dynamic geography mapping, real-time flight data retrieval, persistent data storage, cost-optimized API caching, and LLM-driven market analysis.

The project demonstrates advanced software engineering and AI integration, utilizing the OpenAI API for multi-agent orchestration, Pydantic for strict structured data validation, SerpApi for live web scraping, SQLite for relational data persistence, and Docker / GitHub Actions for modern CI/CD pipelines.

## 📖 Project Description

The main goal of this app is to act as your personal, ruthless travel analyst. Instead of manually searching through dates and airports, you simply enter your desired route (e.g., "Poland - Nicosia"). The AI automatically figures out the best airports to check (e.g., LCA/PFO for Nicosia), estimates standard market prices and ground transport costs, fetches live data from Google Flights, and gives you a strict 1-10 score with pros and cons for every option based on the **Total Estimated Cost**.

## ✨ Key Features

* **Multi-Agent Collaboration**: Two distinct AI agents working together (a Planner and an Analyst) to cross-reference historical estimates with live API data.
* **Smart API Caching (Cost Optimization)**: Built-in 24-hour local cache via SQLite prevents duplicate paid API calls for identical routes, saving credits and significantly speeding up execution.
* **Relational Data Persistence**: All AI evaluations and flight records are automatically saved to a local SQLite database, creating a permanent historical record of your travel deals.
* **Hidden Costs Analysis**: The Planner Agent automatically detects when ground transport is needed (e.g., landing in Larnaca to visit Nicosia) and estimates bus/train costs, forcing the Analyst Agent to evaluate the *total* trip cost, not just the flight ticket.
* **Dynamic Geography & Routing**: Automatically resolves natural language inputs to the most optimal IATA airport codes, including nearby transit hubs. 
* **Strict JSON Outputs**: Uses OpenAI's Structured Outputs and Pydantic to prevent LLM hallucinations and guarantee consistent data models.
* **Docker Containerization**: Fully containerized environment ensuring the app runs flawlessly on any machine.
* **Automated Testing & CI**: Implementation of pytest with mock data to prevent credit consumption, paired with GitHub Actions for Continuous Integration.

## 🏗️ Architecture & Project Structure

The project strictly follows a Modular Multi-Agent pattern, separating API tools, database management, and LLM business logic into dedicated packages:

### 📂 Folder Structure

```text
Flight-Gem-Finder/
├── agents/                 # AI Logic & LLM Prompts
│   ├── __init__.py
│   ├── ai_planner.py       # Agent 1: Geography, Routes & Ground Transport
│   └── ai_analyst.py       # Agent 2: Data Evaluation & Total Cost Scoring
├── core/                   # Utilities & External Integrations
│   ├── __init__.py
│   ├── api_client.py       # External Tool: Google Flights API via SerpApi
│   └── database.py         # SQLite DB Manager: History & API Caching
├── tests/                  # Automated Test Suite
│   ├── __init__.py
│   └── test_api.py         # Pytest with mocked external requests
├── scripts/                # Helper Scripts
│   └── view_db.py          # Utility script to inspect local database records
├── main.py                 # Application entry point & orchestration
├── Dockerfile              # Docker image configuration
├── .dockerignore           # Files excluded from Docker build
├── .gitignore              # Files excluded from version control
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── flights_history.db      # Local SQLite database (Auto-generated, ignored in Git)
└── .env                    # Environment secrets (Local only, ignored in Git)
```

## ⚙️ Configuration (.env)

Ensure a `.env` file is located in the root directory. Never commit this file to your public repository.

```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
SERPAPI_KEY=YOUR_SERPAPI_KEY
```

## 📥 Deployment & Usage

### Option A: Run via Docker (Recommended)

1. **First, clone the repository to your local machine:**

     ```bash
    git clone https://github.com/AntekKozlowski/Flight-Gem-Finder.git
    cd Flight-Gem-Finder
    ```

3.  **Build the image:**

    ```bash
    docker build -t flight-agents .
    ```

4.  **Run the container (passing the .env file):**

    ```bash
    docker run --env-file .env -it flight-agents
    ```

### Option B: Run locally with Python

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    python main.py
    ```

## 🧪 Testing & Continuous Integration

This project uses `pytest` for unit testing and `unittest.mock` to simulate API responses without spending SerpApi credits.

### To run tests locally:

```bash
pytest
```

### Continuous Integration (CI):

Every push or pull request to the `main` branch automatically triggers the GitHub Actions pipeline, setting up a Python environment and running the test suite to ensure code integrity.

## 👨‍💻 Author
Antoni Kozłowski, Cybersecurity Student

