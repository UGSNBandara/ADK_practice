from google.adk.agents import Agent
from google.adk.tools import google_search

news_analyzer = Agent(
    name="news_analyzer",
    model="gemini-2.0-flash",
    description="News Analyzer",
    instruction="""
    You are a news analyzer and you should give the updated news users asking about useing google search tool
    and dont give any responses out of you responsibility.
    
    if asking something out of your range please delegate back to the manager agent
    """,
    tools=[google_search]
)