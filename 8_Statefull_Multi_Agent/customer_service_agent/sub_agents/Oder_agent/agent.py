from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def get_refund_percentage(id:str , tool_context:ToolContext) -> dict:
    """This function check the eligibility to get refond for the course, if eligible output the refund percentage

    Args:
        id (str): course id
        tool_context (ToolContext): context for access and updating session state

    Returns:
        dict: output state
    """
    
    
    courses_p = tool_context.state.get("purchased_courses", [])
    course = {}
    
    if not courses_p:
        return {
            "status" : "Erro",
            "error" : "no any purchased courses",
        }
        
    for item in courses_p:
        if item['id'] == id:
            course = item
            
    if not course:
        return{
            "status" : "error",
            "error" : "This course is not avaible in the purchased list.",
            "course_id" : id
        }
        
    complete_p = course['percentage']
    if complete_p > 50:
        return {
            "state" : "Cant get refund",
            "reason" : "You have completed 50 % of the course so you not eligible to get the refund.",
            "course_id" : id,
        }
    
    return{
        "state" : "You can get the refund",
        "percentage" : 100 - complete_p,
        "description" : f"You can get the {100-complete_p} of percentage form the cource price",
        "course_id" : id,
    }
    
    
def refund(id:str, tool_context : ToolContext) -> dict:
    """
    To get the rufund for the couse:
    
    input:
    id (str): id of the course
    tool_context (ToolContext) : context for accessing and updating memory state
    
    output:
    dict : confiming the refund 
    """
    
    courses_p = tool_context.state.get("purchased_courses", [])
    course_updated = []
    
    for item in courses_p:
        if item['id'] != id:
            course_updated.append(item)
        
    tool_context.state['purchased_courses'] = course_updated
    
    return {
        "state"  : "Successfully refund",
        "description" : "successfully refunmerd the course",
        "course_id" : id,
    } 
    
    
Oder_agent = Agent(
    name="Oder_agent",
    model="gemini-2.0-flash",
    description="This agent is to help to refun courses",
    instruction="""
    You are an helpfull assistant who help to user to refund courses.
    
    you can chech the refund abiliti of the courses user want to refund.
    if they confirm refund you can refund them.
    
    if the user ask for anyhtin out of your scope just delegate it to the custo
    
    procedure :
    
    1 first you have to check whether the mentioned courser user have purchased.
    2 then have to check the refund ability using get_refund_percentage. If able this function retunr the refund percentage
    (normaly if the percentage of completeess below the 50% users may able to get efund based on the completence of the courses)
    4 then after user confirm to refun you can refund the course using refund  tool.
    
    make sure to always get the confirmation before refund any course. if the want to check any details fo the course before refund delegate to the agen, Course_support_agent via manger( customer_service_Agent )
    
    session state these information stored in:
    -Name: {user_name}
    -Purchased Courses list of dictionaries: {purchased_courses}
    
    tools:
    get_refund_percentage : to check the ability to get refund for relevent course: if yes it give the percenatage of amout user can get refund for the course
    refund : to refund course.
    
    """,
    tools=[get_refund_percentage, refund],
)
    