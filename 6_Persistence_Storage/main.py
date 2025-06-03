import asyncio

from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from Reminder_Agent import Reminder_Agent
from utils import call_agent_async
from dotenv import load_dotenv

load_dotenv()

#define the Databasesession
# can use any databse Maria DB also possible ok
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)


initial_state = {
    "username" : "Sulitha",
    "reminders" : [],
}

async def main_as():
    #constants
    APP_NAME = "Sulitha's Reminder"
    USER_ID = "suli119"
    
    existing_session = session_service.list_sessions(
        app_name = APP_NAME,
        user_id = USER_ID,
    )
    
    if existing_session and len(existing_session.sessions)>0:
        
        #get the avaible most reasont session
        session_id  = existing_session.sessions[0].id
        print(f"Continue the existing session : {session_id}")
    
    else:
        
        new_session = session_service.create_session(
            app_name= APP_NAME,
            user_id= USER_ID,
            state= initial_state,
        )        
        
        session_id = new_session.id
        print(f"Start with a new session : {session_id}")
        
    runner = Runner(
        agent=Reminder_Agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
        
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        user_input = input("User : ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Session Ended and State hase been saved to the memory")
            break
        
        await call_agent_async(runner=runner, user_id=USER_ID, session_id=session_id, query=user_input)
        

if __name__ == "__main__":
    asyncio.run(main_as())