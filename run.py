import asyncio
from typing import Any, Dict

from langchain_core.messages import HumanMessage

from src.configuration import Configuration
from src.rpa_graph import graph
from src.states import InputState, UserData


async def main():
    # Initialize user data
    user_data = UserData(
        fields={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "date_of_birth": "1997-10-19",
            "streetAddress": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001",
            "preferredContact": "email",
            "newsletter": True,
        }
    )

    # Create input state
    input_state = InputState(url="http://127.0.0.1:8000", user_data=user_data)

    config = {"recursion_limit": 100}

    try:
        print("Starting RPA workflow...")
        result = await graph.ainvoke(input_state, config=config)
        print("\nWorkflow completed successfully!")
        print("Result:", result)

    except Exception as e:
        print(f"\nError in workflow execution: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
