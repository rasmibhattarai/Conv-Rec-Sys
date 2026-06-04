import time
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

    print("\n=== Welcome to the Appliance Recommender V2 ===")
    print("Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["quit", "exit"]:
                break

            turn_start = time.time()
            logger.debug("--- [TURN START] ---")
            logger.debug(f"--> [CURRENT STATE BEFORE RUN] {deps.model_dump()}")

            start_run = time.time()
            result = await agent.run(
                user_input, deps=deps, message_history=message_history
            )
            logger.debug("--> [RUN COMPLETE]")
            logger.debug(
                f"[TIME] agent.run() completed in {time.time() - start_run:.3f}s"
            )
            logger.debug(f"--> [CURRENT STATE AFTER RUN] {deps.model_dump()}")
            logger.debug(
                f"[TIME] Full turn (user query to assistant response) completed in {time.time() - turn_start:.3f}s"
            )

            message_history = result.all_messages()

            print(f"\nAssistant: {result.output}")
        except EOFError:
            break
        except Exception as e:
            logger.error(f"--> [ERROR] {e}")


if __name__ == "__main__":
    asyncio.run(run_cli())
