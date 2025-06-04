from google.adk.agents import Agent
import random

def get_dad_joke():
    """
    return random one dad's joke
    """
    dad_jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What do you call a fake noodle? An impasta.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
    "What do you call a fish with no eyes? Fsh.",
    "Why did the bicycle fall over? Because it was two-tired.",
    "I used to be a baker, but I couldn't make enough dough.",
    "How do you organize a space party? You planet.",
    "What's orange and sounds like a parrot? A carrot.",
    "My dad told me a joke about a box. I hope it isn't too corny.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "I'm on a seafood diet. I see food and I eat it.",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
    "Why did the coffee file a police report? It got mugged.",
    "I only know 25 letters of the alphabet. I don't know Y.",
    "What do you call a sad strawberry? A blueberry.",
    "Parallel lines have so much in common. It's a shame they'll never meet."
    ]
    
    return random.choice(dad_jokes)
    


dad_joker = Agent(
    name="dad_joker",
    model="gemini-2.0-flash",
    description="Dad's Joke agent",
    instruction="""
    The dad_joker submodel is a sub model which tell and explain about dad's jokes
    and can get the availble dad jokes useing get_dad_joke tool
    
    if asking something out of your range please delegate back to the manager agent
    """,
    tools=[get_dad_joke]
)