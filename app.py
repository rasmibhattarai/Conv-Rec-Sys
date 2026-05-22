import os
import sqlite3
import asyncio
import time
from typing import Optional, List
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI

# 1. Setup & Environment
load_dotenv()
model_name = os.getenv("OPENAI_MODEL", "qwen-3.5-397b")
base_url = os.getenv("OPENAI_BASE_URL")
api_key = os.getenv("OPENAI_API_KEY")

print(
    f"--> [INIT] Initializing OpenAIChatModel with model='{model_name}', base_url='{base_url}'"
)

# Provider for the main agent
provider = OpenAIProvider(base_url=base_url, api_key=api_key)
model = OpenAIChatModel(model_name, provider=provider)

# Standard AsyncOpenAI client for the SQL Sub-Agent
oai_client = AsyncOpenAI(
    api_key=api_key, base_url=base_url.rstrip("/") if base_url else None
)


# 2. State Management (V2 Flexible State)
class AppliancePreferences(BaseModel):
    categories: List[str] = Field(default_factory=list)
    budget: Optional[str] = Field(
        default=None,
        description="String representation of budget, e.g. 'under 1000' or 'between 400 and 800'",
    )
    mandatory_filters: List[str] = Field(default_factory=list)
    soft_preferences: List[str] = Field(default_factory=list)


# 3. The Main Agent
agent = Agent(
    model,
    deps_type=AppliancePreferences,
    system_prompt=(
        "You are a helpful home appliance retail assistant. "
        "Your goal is to understand the user's requirements and recommend products. "
        "You track the user's preferences for: categories (tvs, fridges, washing_machines, dishwashers), budget, mandatory filters (hard constraints), and soft preferences. "
        "Use the `update_preferences` tool to save ANY information the user provides. "
        "Once you have gathered enough information (at least knowing the categories), use the `search_appliances` tool to query the database. "
        "Always present the final recommendations as a short, concise bulleted list. "
        "Do not use long sentences. Keep interactions brief and helpful.\n\n"
        "CRITICAL RULES:\n"
        "1. If the user asks for items that do not exist in our store (e.g., fans, microwaves, diamonds, cars), DO NOT call `update_preferences` with those items. Politely inform them that we only sell TVs, fridges, washing machines, and dishwashers.\n"
        "2. If the user updates ANY of their preferences (budget, filters, categories, etc.), you MUST call the `update_preferences` tool AND THEN immediately call the `search_appliances` tool again to get the fresh data. Do NOT try to filter previous results yourself; always let the database perform the filtering."
    ),
)


# 4. Tools
@agent.tool
def update_preferences(
    ctx: RunContext[AppliancePreferences],
    categories: Optional[List[str]] = None,
    budget: Optional[str] = None,
    mandatory_filters: Optional[List[str]] = None,
    soft_preferences: Optional[List[str]] = None,
) -> str:
    """Use this tool to update the user's preferences whenever they provide new information."""
    start = time.time()
    print(
        f"\n  --> [THOUGHT/TOOL: update_preferences] Extracted args: categories={categories}, budget={budget}, mandatory_filters={mandatory_filters}, soft_preferences={soft_preferences}"
    )

    if categories:
        ctx.deps.categories = list(set(ctx.deps.categories + categories))
    if budget:
        ctx.deps.budget = budget
    if mandatory_filters:
        ctx.deps.mandatory_filters = list(
            set(ctx.deps.mandatory_filters + mandatory_filters)
        )
    if soft_preferences:
        ctx.deps.soft_preferences = list(
            set(ctx.deps.soft_preferences + soft_preferences)
        )

    print(f"  --> [STATE UPDATED] Current state: {ctx.deps.model_dump()}")
    print(
        f"  --> [TIME] Tool 'update_preferences' executed in {time.time() - start:.3f}s"
    )
    return f"Preferences updated successfully. Current state is now: {ctx.deps.model_dump()}"


@agent.tool
async def search_appliances(ctx: RunContext[AppliancePreferences]) -> str:
    """Use this tool to search the database using the currently known preferences."""
    start_tool = time.time()
    print(
        f"\n  --> [THOUGHT/TOOL: search_appliances] Triggered with state: {ctx.deps.model_dump()}"
    )

    if not ctx.deps.categories:
        print("  --> [DB ERROR] Cannot search without a category.")
        return "Error: Category is required to search the database. Ask the user."

    # Schema for the Sub-Agent
    schema = """
    CREATE TABLE tvs (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, resolution TEXT, features TEXT);
    CREATE TABLE fridges (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    CREATE TABLE washing_machines (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    CREATE TABLE dishwashers (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    """

    prompt = f"""You are an expert SQL writer for SQLite.
    Write a SQL query that retrieves products matching these constraints:
    - Categories requested: {ctx.deps.categories}
    - Budget constraint: {ctx.deps.budget}
    - Mandatory filters: {ctx.deps.mandatory_filters}
    - Soft preferences: {ctx.deps.soft_preferences}
    
    Important Rules:
    1. You must ALWAYS retrieve all available columns for the requested items (e.g., use SELECT * or select all specific columns) so that no specifications are missing. If joining multiple tables, ensure all columns from all relevant tables are selected.
    2. Output ONLY the raw SQL query. Do not wrap it in markdown formatting like ```sql ... ```. No explanations.
    3. Be lenient with text searches (e.g. use LIKE '%text%'). 
    4. Make sure your column names strictly match the schema provided below.
    5. Construct the best possible SQL query (e.g., JOINs, subqueries) to accurately satisfy the budget and filter constraints across the requested categories.

    Schema:
    {schema}
    """

    try:
        print("  --> [SQL SUB-AGENT] Requesting SQL generation from LLM...")
        start_llm = time.time()
        response = await oai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        print(f"  --> [TIME] LLM call completed in {time.time() - start_llm:.3f}s")

        raw_query = response.choices[0].message.content.strip()
        # Clean up in case the LLM ignores instructions and outputs markdown
        if raw_query.startswith("```"):
            raw_query = raw_query.split("\n", 1)[-1]
            if raw_query.endswith("```"):
                raw_query = raw_query[:-3]

        query = raw_query.strip()
        print(f"  --> [DB QUERY] Dynamically generated SQL:\n{query}")

        with sqlite3.connect("appliances.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            start_db = time.time()
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"  --> [TIME] DB query executed in {time.time() - start_db:.3f}s")

            if not rows:
                print("  --> [DB RESULTS] No matching items found.")
                return "No matching items found."

            results = [dict(row) for row in rows]
            # Limit results string size slightly just in case it's massive
            if len(results) > 15:
                print(
                    f"  --> [DB RESULTS] Found {len(results)} item combinations. Limiting to top 15 for output."
                )
                results = results[:15]
            else:
                print(f"  --> [DB RESULTS] Found {len(results)} item combinations.")

            print(
                f"  --> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
            )
            return str(results)
    except Exception as e:
        print(f"  --> [DB ERROR] {e}")
        return f"Database error while searching: {e}"


# 5. CLI Loop
async def main():
    deps = AppliancePreferences()
    message_history = []

    print("\n=== Welcome to the Appliance Recommender V2 ===")
    print("Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            print(f"\n--- [TURN START] ---")
            print(f"--> [CURRENT STATE BEFORE RUN] {deps.model_dump()}")

            start_run = time.time()
            result = await agent.run(
                user_input, deps=deps, message_history=message_history
            )
            print(f"\n--> [RUN COMPLETE]")
            print(f"[TIME] agent.run() completed in {time.time() - start_run:.3f}s")
            print(f"--> [CURRENT STATE AFTER RUN] {deps.model_dump()}")

            message_history = result.all_messages()

            print(f"\nAssistant: {result.output}")
        except EOFError:
            break
        except Exception as e:
            print(f"\n--> [ERROR] {e}")


if __name__ == "__main__":
    asyncio.run(main())
