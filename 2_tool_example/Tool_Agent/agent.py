from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def current_time ()-> dict:
    """
        This function output the current date and the time as a dictionary
    """
    return{
        "Current Time" : datetime.now().strftime("%y-%m-%d %H.%M.%S")
    }
    
    

root_agent = Agent(
    name = "Tool_Agent",
    model = "gemini-2.0-flash",
    description="",
    instruction= """
        you are a help full agents give the answer using following tools:
        - google_search
    """,
    tools=[google_search],
)