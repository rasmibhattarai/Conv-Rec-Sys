import os
import sqlite3
import asyncio
from typing import Optional, Literal
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# 1. Setup & Environment
load_dotenv()
model_name = os.getenv("OPENAI_MODEL", "qwen-3.5-397b")
base_url = os.getenv("OPENAI_BASE_URL")
api_key = os.getenv("OPENAI_API_KEY")

print(
    f"--> [INIT] Initializing OpenAIChatModel with model='{model_name}', base_url='{base_url}'"
)

provider = OpenAIProvider(base_url=base_url, api_key=api_key)
model = OpenAIChatModel(model_name, provider=provider)


# 2. State Management
class AppliancePreferences(BaseModel):
    category: Optional[Literal["tvs", "fridges", "washing_machines", "dishwashers"]] = (
        Field(default=None)
    )
    price: Optional[int] = Field(default=None)
    size: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    warranty: Optional[str] = Field(default=None)


# 3. The Agent
agent = Agent(
    model,
    deps_type=AppliancePreferences,
    system_prompt=(
        "You are a helpful home appliance retail assistant. "
        "Your goal is to recommend products to the user based on their preferences. "
        "You track the user's preferences for: category, price (maximum limit), size, type, and warranty. "
        "Use the `update_preferences` tool to save ANY information the user provides. "
        "If you don't know the category, you must ask for it. "
        "Once you have enough information (at least a category), use the `search_appliances` tool to query the database. "
        "Always present the final recommendations as a short, concise bulleted list. "
        "Do not use long sentences. Keep interactions brief and helpful."
    ),
)


# 4. Tools
@agent.tool
def update_preferences(
    ctx: RunContext[AppliancePreferences],
    category: Optional[
        Literal["tvs", "fridges", "washing_machines", "dishwashers"]
    ] = None,
    price: Optional[int] = None,
    size: Optional[str] = None,
    type: Optional[str] = None,
    warranty: Optional[str] = None,
) -> str:
    """Use this tool to update the user's preferences whenever they provide new information."""
    print(
        f"\n  --> [THOUGHT/TOOL: update_preferences] Extracted args: category={category}, price={price}, size={size}, type={type}, warranty={warranty}"
    )

    if category:
        ctx.deps.category = category
    if price:
        ctx.deps.price = price
    if size:
        ctx.deps.size = size
    if type:
        ctx.deps.type = type
    if warranty:
        ctx.deps.warranty = warranty

    print(f"  --> [STATE UPDATED] Current state: {ctx.deps.model_dump()}")
    return f"Preferences updated successfully. Current state is now: {ctx.deps.model_dump()}"


@agent.tool
def search_appliances(ctx: RunContext[AppliancePreferences]) -> str:
    """Use this tool to search the database using the currently known preferences."""
    print(
        f"\n  --> [THOUGHT/TOOL: search_appliances] Triggered with state: {ctx.deps.model_dump()}"
    )

    if not ctx.deps.category:
        print("  --> [DB ERROR] Cannot search without a category.")
        return "Error: Category is required to search the database. Ask the user."

    query = f"SELECT * FROM {ctx.deps.category} WHERE 1=1"
    params = []

    if ctx.deps.price is not None:
        query += " AND price <= ?"
        params.append(ctx.deps.price)
    if ctx.deps.size is not None:
        query += " AND size = ?"
        params.append(ctx.deps.size)
    if ctx.deps.type is not None:
        query += " AND type = ?"
        params.append(ctx.deps.type)
    if ctx.deps.warranty is not None:
        query += " AND warranty = ?"
        params.append(ctx.deps.warranty)

    print(f"  --> [DB QUERY] Executing: '{query}' with params {params}")

    try:
        with sqlite3.connect("appliances.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                print("  --> [DB RESULTS] No matching items found.")
                return "No matching items found."

            results = [dict(row) for row in rows]
            print(f"  --> [DB RESULTS] Found {len(results)} items.")
            return str(results)
    except Exception as e:
        print(f"  --> [DB ERROR] {e}")
        return f"Database error: {e}"


# 5. CLI Loop
async def main():
    deps = AppliancePreferences()
    message_history = []

    print("\n=== Welcome to the Appliance Recommender ===")
    print("Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            print(f"\n--- [TURN START] ---")
            print(f"--> [CURRENT STATE BEFORE RUN] {deps.model_dump()}")

            result = await agent.run(
                user_input, deps=deps, message_history=message_history
            )

            print(f"\n--> [RUN COMPLETE]")
            print(f"--> [CURRENT STATE AFTER RUN] {deps.model_dump()}")

            message_history = result.all_messages()

            print(f"\nAssistant: {result.output}")
        except EOFError:
            break
        except Exception as e:
            print(f"\n--> [ERROR] {e}")


if __name__ == "__main__":
    # In some async environments (like Jupyter), you might need nested asyncio loops,
    # but standard `asyncio.run()` is fine for CLI scripts.
    asyncio.run(main())
