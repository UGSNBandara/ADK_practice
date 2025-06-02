from google.adk.agents import Agent

answer_agent = Agent(
    name="answer_agent",
    model="gemini-2.0-flash",
    description="Basic answering agent based on the user name and preference",
    instruction="""
    Give the answer for the questions based on the user name and the user pre defined preferences
    
    You can get the name and preference from state by key : 
    
    name = {username}
    preferences = {userpreference}
    
    """
)  