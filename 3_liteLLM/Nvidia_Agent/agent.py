import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="nvidia_nim/tiiuae/falcon3-7b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"), 
)

def get_dad_jokes () -> str:
    dad_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "How does a penguin build its house? Igloos it together!",
    "Why did the bicycle fall over? Because it was two-tired.",
    "Did you hear about the guy who invented Lifesavers? He made a mint.",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why couldn't the leopard play hide and seek? Because he was always spotted.",
    "I'm reading a book on anti-gravity. It's impossible to put down."
    ]

    return random.choice(dad_jokes)


root_agent = Agent(
    name="Nvodoa_Agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    Your are agent which can tell dad jokens ( common dads jokes) 
    """,
    #tools=[get_dad_jokes]
    #seems like nvidia model not help to function calling ? 
)