import asyncio

from dotenv import load_dotenv
from customer_service_agent.agent import customer_service_agent 
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import  call_agent_async



load_dotenv()

initial_state = {
    "user_name" : "Sulitha Nulaksha",
    "purchased_courses" : [
        {"id": "C002","purchased_date": "2025-05-6","percentage" : 0},
        {"id": "C003","purchased_date": "2025-05-10","percentage" : 50},
        ],
}

session_service = InMemorySessionService()


async def main_async():
    
    APP_NAME = "Customer Support"
    USER_ID = "aiwithbrandon"

    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    print("\nWelcome to Customer Service Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()