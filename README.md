# ✈️ Flight Gem Finder (Multi-Agent AI System)

![Status](https://img.shields.io/badge/Status-Stable-green)
![Language](https://img.shields.io/badge/language-Python_3.11-blue)
![Architecture](https://img.shields.io/badge/architecture-Multi--Agent-orange)
![Container](https://img.shields.io/badge/platform-Docker-blue)
![Testing](https://img.shields.io/badge/testing-Pytest-yellowgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Flight Gem Finder is an autonomous, high-performance Multi-Agent AI System designed to act as a personal travel analyst. It features dynamic geography mapping, real-time flight data retrieval, LLM-driven market analysis, and full containerization.

The project demonstrates advanced software engineering and AI integration, utilizing the OpenAI API for multi-agent orchestration, Pydantic for strict structured data validation, SerpApi for live web scraping, and Docker / GitHub Actions for modern CI/CD pipelines.

## 📖 Project Description

The main goal of this app is to act as your personal, ruthless travel analyst. Instead of manually searching through dates and airports, you simply enter your desired route (e.g., "Poland - Bali"), select one-way or round-trip, and input your dates. The AI automatically figures out the best airports to check, estimates standard market prices based on its internal knowledge, fetches live data from Google Flights, and gives you a strict 1-10 score with pros and cons for every option.

## ✨ Key Features

*   **Multi-Agent Collaboration**: Two distinct AI agents working together (a Planner and an Analyst) to cross-reference historical estimates with live API data.
*   **Dynamic Geography & Routing**: Automatically resolves natural language inputs (e.g., "Poland to Bali") to the most optimal IATA airport codes, including nearby transit hubs. Supports both one-way and round-trip logic.
*   **Strict JSON Outputs**: Uses OpenAI's Structured Outputs and Pydantic to prevent LLM hallucinations and guarantee consistent data models.
*   **Live Data Fetching**: Scrapes real-time prices, carrier info, and layover durations using SerpApi (Google Flights engine).
*   **Docker Containerization**: Fully containerized environment ensuring the app runs flawlessly on any machine without local dependency issues.
*   **Automated Testing & CI**: Implementation of pytest with API mocking to prevent credit consumption, paired with GitHub Actions for Continuous Integration.

## 🏗️ Architecture & Project Structure

The project strictly follows a Multi-Agent pattern, separating API tools from LLM decision-making and business logic:

*   **Agent 1: Planner** (`ai_planner.py`): Translates human intent into structured API queries. It uses LLM knowledge to establish a baseline market price and a "gem threshold."
*   **Tool: API Client** (`api_client.py`): The hands of the operation. It connects to the outside world via SerpApi to fetch hard, live data.
*   **Agent 2: Analyst** (`agent.py`): The brain of the operation. It processes the live data against the Planner's baselines, calculates a score, and makes a final verdict on the flight's quality using Pydantic.

### 📂 Folder Structure

```text
Flight-Gem-Finder/
├── .github/
│   └── workflows/
│       └── test.yml        # GitHub Actions CI pipeline
├── ai_planner.py           # Agent 1: Planning & Geography
├── agent.py                # Agent 2: Analysis & Verdict
├── api_client.py           # Tool: External API integration
├── main.py                 # Application entry point
├── test_api.py             # Automated unit tests (Pytest)
├── Dockerfile              # Docker image configuration
├── .dockerignore           # Files excluded from Docker build
├── requirements.txt        # Project dependencies
└── .env                    # Environment secrets (Local only)
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
    docker build -t flight-agent .
    ```

4.  **Run the container (passing the .env file):**

    ```bash
    docker run --env-file .env -it flight-agent
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

Every push or pull request to the `main` or `master` branch automatically triggers the GitHub Actions pipeline, setting up a Python environment and running the test suite to ensure code integrity.

## 👨‍💻 Author
Antoni Kozłowski, Cybersecurity Student

