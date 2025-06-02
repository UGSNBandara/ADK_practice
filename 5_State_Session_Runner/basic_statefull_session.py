import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from answer_agent import answer_agent

load_dotenv()

session_service = InMemorySessionService()

initial_satate = {
    "username" : "Sulitha Nulaksha",
    "userpreference" : """
        Like to explote AI and ML updates.
        Like to watch movies and fav movie series is Pirates of the Caribian.
        I am Mix of Extrovert and introvers, but mostly like to live alone.
        love to the calm and peace
    """,
}

APP_NAME = "Sulitha't Personal bot"
USER_ID = "Sulithas_Personal_Bot"
SESSION_ID = str(uuid.uuid4())

stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_satate,
)


runner = Runner(
    agent=answer_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is he do when his favourite time ? ")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Res : {event.content.parts[0].text}")