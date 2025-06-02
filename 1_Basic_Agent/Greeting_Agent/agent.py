from google.adk.agents import Agent

root_agent = Agent(
    name="Greeting_Agent",
    model = "gemini-2.0-flash",
    description = "Greeting Agent",
    instruction = """
        Your are a greeting agent and ask
        for the user's name and greet them by name
    """,
)