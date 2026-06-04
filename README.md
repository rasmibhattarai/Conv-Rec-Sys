# AI Appliance Recommender

This project is a conversational recommendation system that helps users shop for home appliances like TVs, fridges, washing machines, and dishwashers.

On the technical side, it uses an AI agent built with `pydantic-ai` to chat with users and remember their preferences. When you ask for something in natural language (like "I need a TV under $500"), the agent doesn't just guess. Instead, it translates your chat into a SQL query on the fly, and then searches a local SQLite database to find real, exact products that match what you're looking for.

## Features

- **Conversational Interface**: Ask for products in plain English (e.g., "I want a 4K TV under $500").
- **Dynamic SQL Generation**: A sub-agent automatically translates your requests into SQLite queries to filter the product catalog.
- **State Management**: Keeps track of your preferences (categories, budget, mandatory filters) across the conversation.
- **Modular Architecture**: Clean separation of configuration, state, database logic, AI tools, and the main agent.

## Prerequisites

- Python 3.8+
- An OpenAI-compatible API key (can be OpenAI, or a custom inference endpoint).

## Installation

1. **Clone the repository** and navigate to the project directory.

2. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your API credentials:
   ```env
   OPENAI_MODEL=your preferred model (e.g., gpt-4o)
   OPENAI_BASE_URL=https://your-api-endpoint.com/v1
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Initialize the Database**:
   The `appliances.db` SQLite database tracks our inventory. You can reset or re-initialize it at any time by running:
   ```bash
   python db/init_db.py
   ```
   You can verify the database is working and query some test data with:
   ```bash
   python db/verify_db.py
   ```

## Usage

Start the interactive assistant by running the main entry point:

```bash
python app.py
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

## Project Structure

```text
├── app.py                 # Main entry point to run the CLI loop
├── db/                    # Database storage and scripts
│   ├── appliances.db      # SQLite database file
│   ├── init_db.py         # Script to initialize/reset the database
│   ├── init_db.sql        # SQL schema and seed data
│   └── verify_db.py       # Script to verify DB functionality
├── requirements.txt       # Project dependencies
└── src/                   # Application source code
    ├── __init__.py
    ├── agent.py           # Core Pydantic-AI agent and system prompt
    ├── config.py          # Environment, API, and logger configuration
    ├── database.py        # Database execution and SQL prompt logic
    ├── main.py            # CLI event loop
    ├── state.py           # Pydantic models for user preferences state
    └── tools.py           # AI tools (update_preferences, search_appliances)
```