from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.dad_joker.agent import dad_joker
from .sub_agents.news_analyzer.agent import news_analyzer
from .sub_agents.wheather_analyzer.agent import wheather_analyzer
from .tools.tools import get_current_time


root_agent = Agent(
    name="Manager",
    model="gemini-2.0-flash",
    description="Manger agent",
    instruction="""
    You are the manager agent and your responsible for overseeing the subagents.
    
    you have to delegate the tasks to appropriate sub agent availble.
    if you can do the task do by your self other wise delegate to the specific sub agent.
    
    if the query out of the box, just tell you cant do it.
    
    sub_agents : 
    dad_joker
    wheather_analyzer
    
    other tools you can access:
    get_current_time
    news_analyzer
    """,
    sub_agents=[dad_joker, wheather_analyzer],
    tools=[get_current_time, AgentTool(news_analyzer)],
)