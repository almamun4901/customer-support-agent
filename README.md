# 🤖 AI Customer Support Agent

An intelligent customer support agent built with **LangGraph**, **Claude (Anthropic)**, and **ChromaDB**. The agent automatically triages incoming support tickets, retrieves relevant knowledge base context, determines escalation needs, generates AI-powered responses, and logs tickets to a database.

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Agent Workflow](#-agent-workflow)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Configuration](#-configuration)
- [API Usage](#-api-usage)
- [Testing](#-testing)
- [Escalation Logic](#-escalation-logic)

---

## 🏗 Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Client  │────▶│  FastAPI API  │────▶│ LangGraph │
└──────────┘     └──────────────┘     │  Workflow │
                                      └─────┬────┘
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                 ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
                 │  Claude LLM │   │   ChromaDB   │   │    SQLite    │
                 │  (Anthropic)│   │ (Vector Store)│   │  (Tickets)  │
                 └─────────────┘   └──────────────┘   └──────────────┘
```

---

## 🔄 Agent Workflow

The agent follows a **5-step LangGraph pipeline**:

```
START → Triage → Retrieve → Escalation Logic → Generate Response → Create Ticket → END
```

| Step | Description |
|------|-------------|
| **1. Triage** | Claude analyzes the ticket and classifies its `category`, `urgency`, and `sentiment` using structured output |
| **2. Retrieve** | Searches the ChromaDB knowledge base for relevant context using HuggingFace embeddings |
| **3. Escalation Logic** | Determines if the ticket should be escalated based on urgency, sentiment, and category |
| **4. Generate Response** | Claude generates a context-aware response to the customer query |
| **5. Create Ticket** | Saves the ticket with all metadata to the SQLite database |

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | Claude Sonnet 4 (Anthropic) |
| **Agent Framework** | LangGraph |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (local, free) |
| **Vector Database** | ChromaDB |
| **Ticket Database** | SQLite (via SQLAlchemy) |
| **API Framework** | FastAPI |
| **Containerization** | Docker & Docker Compose |
| **Testing** | Pytest |

---

## 📁 Project Structure

```
customer-support-agent/
├── app/
│   ├── config.py        # Pydantic settings (loads .env)
│   ├── graph.py         # LangGraph workflow definition
│   ├── kb.py            # ChromaDB knowledge base (retrieval + ingestion)
│   ├── llm.py           # Claude LLM factory
│   ├── main.py          # FastAPI application & /chat endpoint
│   ├── state.py         # SupportState TypedDict (shared state schema)
│   └── tickets.py       # SQLAlchemy ticket model & CRUD operations
├── tests/
│   ├── test_api.py      # Pytest integration tests
│   └── test_cases.json  # Parameterized test scenarios
├── .env                 # Environment variables (API keys, DB config)
├── .gitignore           # Git ignore rules (ignores .env, .venv, etc.)
├── compose.yaml         # Docker Compose (backend + ChromaDB)
├── Dockerfile           # Python 3.11 container setup
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🚀 Setup & Installation

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- An [Anthropic API key](https://console.anthropic.com/settings/keys)

### 1. Clone the Repository

```bash
git clone https://github.com/almamun4901/customer-support-agent.git
cd customer-support-agent
```

### 2. Configure Environment

Create a `.env` file in the project root (or edit the existing one):

```env
# LLM
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514

# Database
DATABASE_URL=sqlite:///tickets.db

# ChromaDB
CHROMA_HOST=http://chroma:8000
CHROMA_COLLECTION=support_kb

# App
ENVIRONMENT=development
LOG_LEVEL=info
```

### 3. Build & Run with Docker

```bash
docker compose build
docker compose up
```

The API will be available at **http://localhost:8000**.

### 4. (Optional) Set Up Local Environment for Testing

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest requests
```

---

## ⚙️ Configuration

Configuration is managed via **Pydantic Settings** (`app/config.py`), which loads from the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | *required* |
| `CLAUDE_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `DATABASE_URL` | SQLAlchemy database URL | *required* |
| `CHROMA_HOST` | ChromaDB server URL | `http://chroma:8000` |

### Embeddings

This project uses **HuggingFace `all-MiniLM-L6-v2`** for embeddings, which runs **locally** inside the Docker container. **No API key is needed** — the model (~80MB) is downloaded automatically on first startup.

---

## 📡 API Usage

### `POST /chat`

Send a customer support message and receive an AI-generated response.

**Request:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I was charged twice and I am extremely upset."}'
```

**Response:**

```json
{
  "userQuery": "I was charged twice and I am extremely upset.",
  "category": "billing",
  "urgency": "high",
  "sentiment": "negative",
  "kbContext": "",
  "answer": "I sincerely apologize for the duplicate charge...",
  "escalate": true,
  "ticketId": 1
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `userQuery` | `string` | The original customer message |
| `category` | `string` | Classified category (billing, technical, sales, refund, general) |
| `urgency` | `string` | Urgency level (low, medium, high) |
| `sentiment` | `string` | Detected sentiment (positive, negative, neutral) |
| `kbContext` | `string` | Retrieved knowledge base context |
| `answer` | `string` | AI-generated response |
| `escalate` | `boolean` | Whether the ticket requires escalation |
| `ticketId` | `integer` | Database ID of the created ticket |

---

## 🧪 Testing

Tests are located in `tests/` and use **pytest** with parameterized test cases defined in `tests/test_cases.json`.

### Run All Tests

```bash
# Make sure Docker containers are running first
docker compose up -d

# Run tests
source .venv/bin/activate
pytest tests/test_api.py -v
```

### Run a Single Test

```bash
pytest "tests/test_api.py::test_support_agent[case0]" -v
```

### Test Cases

The test suite includes **10 scenarios** covering various support situations:

| # | Scenario | Expected Escalation |
|---|----------|-------------------|
| 0 | Duplicate charge (high urgency) | ✅ Yes |
| 1 | Refund policy question | ❌ No |
| 2 | Shipping delay complaint | ✅ Yes |
| 3 | Password reset issue | ❌ No |
| 4 | Account locked (urgent) | ✅ Yes |
| 5 | General inquiry | ❌ No |
| 6 | Refund angry tone | ✅ Yes |
| 7 | Billing clarification (calm) | ❌ No |
| 8 | Technical minor issue | ❌ No |
| 9 | High urgency refund | ✅ Yes |

---

## 🚨 Escalation Logic

Tickets are escalated based on the following rules:

```python
escalate = (
    urgency == 'high' or
    sentiment == 'negative' or
    (category == 'billing' and (urgency == 'high' or sentiment == 'negative'))
)
```

- **High urgency** → Always escalated
- **Negative sentiment** → Always escalated
- **Billing + high urgency or negative sentiment** → Escalated
- **Billing + calm/neutral** → Not escalated (handled normally)

---

## 📄 License

This project is for educational purposes.

---

## 👤 Author

**Md Al Mamun**
