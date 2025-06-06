from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from datetime import date
from courses import courses

def purchase (id:str, tool_context : ToolContext)-> dict:
    """
    to purchase a course use this tool

    Args:
        id (str): id of the course going to be purchase
        tool_contex (ToolContext): context for accesing and updating session state

    Returns:
        dict: output
    """
    courses_p = tool_context.state.get("purchased_courses", [])

    for items in courses_p:
        if items['id'] == id:
            return{
                "state" : "Already exists the course", # Corrected typo
                "id" : id,
            }

    new_course = {
        "id" : id,
        "purchased_date" : date.today().strftime("%Y-%m-%d"), # Corrected to date.today()
        "percentage" : 0,
        }

    courses_p.append(new_course)

    tool_context.state['purchased_courses'] = courses_p

    return {
        "status" : "Successfully purchased",
        "course" : new_course,
    }

def get_available_courses_code_and_title() -> list:
    """to get the availble courses id and name as list of dictionary

    Returns:
        list : list of dictionaries contain coourse id and name available
    """
    
    courses_details = []
    
    for item in courses:
        new = {"id" : item['id'], "name" : item['name']}
        courses_details.append(new)
    
    return courses_details


def get_detail_of_course_by_id(id:str) -> dict:
    """to get the detailes of specific course by its id

    Args:
        id (str): if of the courses going to get the details

    Returns:
        dict: output
    """
    
    for item in courses:
        if item['id'] == id:
            return item
        
    return{
        "status" : "404error course id not available in the list",
    }


Salse_agent = Agent(
    name="Salse_agent",
    model="gemini-2.0-flash",
    description="Salse agent help to purchase cousers and market the courses and give infotrmation about services",
    instruction="""
    You are a helpull sales agent fot this courses platform and you are responsible for purchses courses, explain about courses, 
    and market but dont rush the customers be friendly and healfull always
    
    you should give the clear details and corses details when asking by the user using tools get_available_courses_code_and_title, get_detail_of_course_by_id
    and when user asking about courses, check whether user has already purchased, using {purchased_courses} session state
    
    if user want to purcase any courses, use the purchase tool and give the course code and tool_context as input to edit and acccess the session state
    
    session state memory:
    
    Name: {user_name}
    Purchased Courses: {purchased_courses}

    tools can use:
        purchase :to purchase the course
        get_available_courses_code_and_title :  to get the avaible courses list wich contain couse name and id
        get_detail_of_course_by_id : to get the course details by the course id    
    """,
    
    tools=[purchase, get_available_courses_code_and_title, get_detail_of_course_by_id]
    
)
        
    