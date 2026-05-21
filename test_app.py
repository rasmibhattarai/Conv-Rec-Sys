import asyncio
from app import agent, AppliancePreferences


async def run_test():
    deps = AppliancePreferences()
    message_history = []

    print("\n--- Test 1: I want to buy a TV ---")
    result = await agent.run(
        "I want to buy a tv", deps=deps, message_history=message_history
    )
    message_history = result.all_messages()
    print(f"Assistant: {result.output}")
    print(f"State: {deps.model_dump()}")

    print("\n--- Test 2: My budget is 400 euros ---")
    result = await agent.run(
        "My budget is 400 euros", deps=deps, message_history=message_history
    )
    message_history = result.all_messages()
    print(f"Assistant: {result.output}")
    print(f"State: {deps.model_dump()}")

    print("\n--- Test 3: Are there any 40 inch ones? ---")
    result = await agent.run(
        "Are there any 40 inch ones?", deps=deps, message_history=message_history
    )
    message_history = result.all_messages()
    print(f"Assistant: {result.output}")
    print(f"State: {deps.model_dump()}")


if __name__ == "__main__":
    asyncio.run(run_test())
