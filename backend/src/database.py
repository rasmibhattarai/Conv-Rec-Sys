import sqlite3
import logging
import os

logger = logging.getLogger(__name__)


def _build_sql_prompt(
    categories, budget, mandatory_filters, soft_preferences, schema, relaxed=False
):
    """Build SQL prompt with optional constraint relaxation."""
    if relaxed:
        prompt = f"""You are an expert SQL writer for SQLite.
Write a SIMPLE SQL query that retrieves products matching these constraints:
- Categories requested: {categories}
- Budget constraint: {budget} (optional - simplify or ignore if complex)
- Mandatory filters: {mandatory_filters} (optional - ignore if complex)
- Soft preferences: {soft_preferences} (ignore)

Important Rules:
1. You must ALWAYS retrieve all available columns (SELECT * or list all columns).
2. Output ONLY the raw SQL query. No markdown, no explanations.
3. Be lenient with text searches (e.g. use LIKE '%text%'). 
4. Make sure your column names strictly match the schema provided below.
5. Prioritize returning products in the requested categories. Simplify budget/filter logic if complex.

Schema:
{schema}
"""
    else:
        prompt = f"""You are an expert SQL writer for SQLite.
Write a SQL query that retrieves products matching these constraints:
- Categories requested: {categories}
- Budget constraint: {budget}
- Mandatory filters: {mandatory_filters}
- Soft preferences: {soft_preferences}

Important Rules:
1. You must ALWAYS retrieve all available columns for the requested items (e.g., use SELECT * or select all specific columns) so that no specifications are missing. If joining multiple tables, ensure all columns from all relevant tables are selected.
2. Output ONLY the raw SQL query. Do not wrap it in markdown formatting like ```sql ... ```. No explanations.
3. Be lenient with text searches (e.g. use LIKE '%text%'). 
4. Make sure your column names strictly match the schema provided below.
5. Construct the best possible SQL query (e.g., JOINs, subqueries) to accurately satisfy the budget and filter constraints across the requested categories.

Schema:
{schema}
"""
    return prompt


def _format_relaxed_results(results, relaxation_level):
    """Format results with user-friendly message about relaxed constraints."""
    messages = {
        1: "Here are some options close to your requirements:",
        2: "Here are available products matching your categories:",
    }
    return f"{messages.get(relaxation_level, 'Here are your results:')}\n{results}"


async def _execute_sql_query(query):
    """Execute SQL query and return results."""
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "db", "appliances.db"
    )
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return []
        results = [dict(row) for row in rows]
        # if len(results) > 15:
        #     results = results[:15]
        return results
