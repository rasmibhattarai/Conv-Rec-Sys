# Home Appliance Recommender

A conversational recommendation system that helps users shop for home appliances like TVs, fridges, washing machines, and dishwashers.

The system uses an AI agent built with `pydantic-ai` to chat with users and remember their preferences. When you ask for something in natural language (like "I need a TV under $500"), the agent translates your request into a SQL query and searches a local SQLite database to find exact matching products.

## Features

- **Conversational Interface**: Ask for products in plain English
- **Dynamic SQL Generation**: Automatically translates requests into SQLite queries
- **State Management**: Tracks preferences (categories, budget, filters) across the conversation
- **Web UI**: Modern React interface with real-time preference sidebar
- **API Backend**: RESTful FastAPI backend for chat interactions
- **Modular Architecture**: Clean separation of configuration, state, database logic, and AI tools

## Project Structure

```
Project/
├── backend/                 # Backend Python application
│   ├── api.py              # FastAPI server entry point
│   ├── app.py              # CLI entry point
│   ├── src/                # Backend source code
│   │   ├── agent.py        # Core Pydantic-AI agent
│   │   ├── config.py       # Environment and API configuration
│   │   ├── database.py     # Database execution and SQL logic
│   │   ├── main.py         # CLI event loop
│   │   ├── state.py        # User preferences state models
│   │   └── tools.py        # AI tools (update_preferences, search_appliances)
│   ├── db/                 # Database storage
│   │   ├── appliances.db   # SQLite database file
│   │   ├── init_db.py      # Database initialization script
│   │   ├── init_db.sql     # SQL schema and seed data
│   │   └── verify_db.py    # Database verification script
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # React web interface
│   ├── src/                # Frontend source code
│   ├── public/             # Static assets
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite configuration
├── .env                    # Your environment variables (not tracked)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Node.js 18+ (for web UI)
- An OpenAI-compatible API key

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Project
```

### 2. Set up Python backend

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up Frontend (optional - for web UI)

```bash
cd frontend
npm install
cd ..
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API credentials:

```env
OPENAI_MODEL=your_preferred_model (e.g., gpt-4o)
OPENAI_BASE_URL=https://your-api-endpoint.com/v1
OPENAI_API_KEY=your_api_key_here
```

### 5. Initialize the Database

```bash
python backend/db/init_db.py
```

Verify the database is working:

```bash
python backend/db/verify_db.py
```

## Usage

### Option 1: Web Interface (Recommended)

**Start the backend API server:**

```bash
source venv/bin/activate  # If not already activated
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**In a separate terminal, start the frontend:**

```bash
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173` (or the URL shown in the terminal).

The web interface includes:
- Chat interface for natural language conversations
- Sidebar showing tracked preferences (categories, budget, filters)
- Real-time updates as preferences change

### Option 2: Command Line Interface

```bash
source venv/bin/activate
python backend/app.py
```

### Example Interaction

```
User: I'm looking for a TV under 500 dollars.
Assistant: Here are some great TV options under $500:
- Hisense 32" LED - $179
- TCL 43" 4K - $329
- Panasonic 55" 4K - $499
Would you like more details on any of these?
```

## API Endpoints

### POST /chat

Send a chat message and receive a response.

**Request:**
```json
{
  "session_id": "optional-uuid",
  "message": "I want a TV under $500"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "response": "Here are some TV options...",
  "state": {
    "categories": ["TV"],
    "budget": "under $500",
    "mandatory_filters": [],
    "soft_preferences": []
  }
}
```

## Configuration

All configuration is managed through environment variables in the `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_MODEL` | Model to use for inference | `gpt-4o`, `qwen-3.5-397b` |
| `OPENAI_BASE_URL` | API endpoint URL | `https://api.openai.com/v1` |
| `OPENAI_API_KEY` | Your API key | `sk-...` |

## Troubleshooting

**Database issues:**
```bash
# Reset the database
python backend/db/init_db.py
```

**Frontend build issues:**
```bash
cd frontend
rm -rf node_modules
npm install
```

**Backend issues:**
```bash
# Check if virtual environment is activated
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```
