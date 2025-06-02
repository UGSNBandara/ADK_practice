from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class EmailOutput(BaseModel):
    subject : str = Field(description="This is the subject of the genarated email")
    body : str = Field(description="This is the body of the genarated email")

root_agent = LlmAgent(
    name="Email_genarate_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are a email genarating assistent and you have to genarate emails based on user requests
        
        email should contain in 2 part:
        subject, and body
        
        email should be a completed and also simple
        
        IMPORTANT: your response must be valid JSON matching stucture:
        {
            "subject" : "Subject line here",
            "body" : "body here"
        }
        Don't include any aidtional text outside the JSON, only the JSON forma output.
    """,
    description="Email genarating agent for given deta, and output should be in given output struture",
    output_schema= EmailOutput,
    output_key="email",
)

