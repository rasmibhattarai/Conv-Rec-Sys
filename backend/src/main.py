import asyncio
import logging
from .agent import agent
from .state import AppliancePreferences

# Import tools to ensure they are registered with the agent
import src.tools

logger = logging.getLogger(__name__)


async def run_cli():
    deps = AppliancePreferences()
    message_history = []

    print("\n=== Welcome to the Appliance Recommender ===")
    print("Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            result = await agent.run(
                user_input, deps=deps, message_history=message_history
            )

            message_history = result.all_messages()

            print(f"\nAssistant: {result.output}")
        except EOFError:
            break
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(run_cli())
