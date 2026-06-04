import time
import asyncio
import logging
from typing import Optional, List
from pydantic_ai import RunContext

from .agent import agent
from .state import AppliancePreferences
from .database import _build_sql_prompt, _format_relaxed_results, _execute_sql_query
from .config import oai_client, model_name

logger = logging.getLogger(__name__)


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
    logger.debug(
        f"--> [THOUGHT/TOOL: update_preferences] Extracted args: categories={categories}, budget={budget}, mandatory_filters={mandatory_filters}, soft_preferences={soft_preferences}"
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

    logger.debug(f"--> [STATE UPDATED] Current state: {ctx.deps.model_dump()}")
    logger.debug(
        f"--> [TIME] Tool 'update_preferences' executed in {time.time() - start:.3f}s"
    )
    return f"Preferences updated successfully. Current state is now: {ctx.deps.model_dump()}"


@agent.tool
async def search_appliances(ctx: RunContext[AppliancePreferences]) -> str:
    """Use this tool to search the database using the currently known preferences."""
    start_tool = time.time()
    logger.debug(
        f"--> [THOUGHT/TOOL: search_appliances] Triggered with state: {ctx.deps.model_dump()}"
    )

    if not ctx.deps.categories:
        logger.debug("--> [DB ERROR] Cannot search without a category.")
        return "Error: Category is required to search the database. Ask the user."

    schema = """
    CREATE TABLE tvs (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, resolution TEXT, features TEXT);
    CREATE TABLE fridges (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    CREATE TABLE washing_machines (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    CREATE TABLE dishwashers (id INTEGER, name TEXT, brand TEXT, type TEXT, size TEXT, price INTEGER, color TEXT, warranty TEXT, energy_rating TEXT, features TEXT);
    """

    max_attempts = 2
    for attempt in range(max_attempts):
        relaxed = attempt == 1

        try:
            prompt = _build_sql_prompt(
                ctx.deps.categories,
                ctx.deps.budget,
                ctx.deps.mandatory_filters,
                ctx.deps.soft_preferences,
                schema,
                relaxed=relaxed,
            )

            logger.debug(
                f"--> [SQL SUB-AGENT] Requesting SQL generation from LLM (attempt {attempt + 1}, relaxed={relaxed})..."
            )
            start_llm = time.time()
            response = await asyncio.wait_for(
                oai_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                ),
                timeout=60.0,
            )
            logger.debug(
                f"--> [TIME] LLM call completed in {time.time() - start_llm:.3f}s"
            )

            raw_query = response.choices[0].message.content.strip()
            if raw_query.startswith("```"):
                raw_query = raw_query.split("\n", 1)[-1]
                if raw_query.endswith("```"):
                    raw_query = raw_query[:-3]

            query = raw_query.strip()
            logger.debug(f"--> [DB QUERY] Dynamically generated SQL:\n{query}")

            start_db = time.time()
            results = await asyncio.wait_for(_execute_sql_query(query), timeout=60.0)
            logger.debug(
                f"--> [TIME] DB query executed in {time.time() - start_db:.3f}s"
            )

            if results:
                logger.debug(
                    f"--> [DB RESULTS] Found {len(results)} item combinations."
                )
                if relaxed:
                    message = _format_relaxed_results(results, 1)
                    logger.debug(
                        f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
                    )
                    return message
                logger.debug(
                    f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
                )
                return str(results)
            else:
                logger.debug("--> [DB RESULTS] No matching items found.")
                if relaxed:
                    logger.debug(
                        f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
                    )
                    return "[SEARCH_FAILED] No matching items found. Show this to the user and ask them to broaden their criteria. Do NOT retry the search."
                continue

        except asyncio.TimeoutError:
            logger.debug(f"--> [TIMEOUT] Attempt {attempt + 1} timed out after 60s.")
            if relaxed:
                logger.debug(
                    f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
                )
                return "[SEARCH_FAILED] Search timed out. Show this to the user and ask them to rephrase with simpler criteria. Do NOT retry the search."
            continue

        except Exception as e:
            logger.debug(f"--> [DB ERROR] {e}")
            if relaxed:
                logger.debug(
                    f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
                )
                return f"[SEARCH_FAILED] Database error: {e}. Show this to the user and ask them to rephrase. Do NOT retry the search."
            continue

    logger.debug(
        f"--> [TIME] Tool 'search_appliances' executed in {time.time() - start_tool:.3f}s"
    )
    return "[SEARCH_FAILED] Search failed after multiple attempts. Show this to the user and ask them to rephrase with simpler criteria. Do NOT retry the search."
