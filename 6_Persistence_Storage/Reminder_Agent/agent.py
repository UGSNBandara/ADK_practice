from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


#we gonna ultilies 5 methods, add, delete, update, view reminder  + change username

def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    
    """
    Add a new reminder to the riminder list in session state
    
    Args:
        reminder : new reminder going to add, type = str
        tool_context : context for accessing and updating session state
        
    Returens : 
        confirm message as a dictionary 
    """
    
    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)
    
    tool_context.state['reminders'] = reminders
    
    print(f"Succcessfully add a new reminder : {reminder} to the reminder list")  
    
    return {
        "action" : "Add_Reminder",
        "reminder" : reminder,
        "message" : f"added reminder : {reminder}",
    }  
    
def view_reminders(tool_context : ToolContext) -> dict:
    
    """
    View the available reminder list
    
    Args : 
    tool_context : Context for accessing the session state
    
    Returns : 
        confirm message with list and count of reminder in a dictionary
    """
    
    reminders = tool_context.state.get("reminders", [])
    
    return {
        "action" : "View_Reminders",
        "reminders" : reminders,
        "counts" : len(reminders),
    }
    

def update_reminder(index : int, new_reminder : str, tool_context : ToolContext) -> dict:
    """
    Update exisitng reminder by new version

    Args:
        index (int): index of the the reminder to be updated, in 1 base indexing
        new_reminder (str): new reminder to be replaced with
        tool_context (ToolContext): context to accessing and updating of session state 

    Returns:
        dict: confirming messages
    """
    
    reminders = tool_context.state.get("reminders", [])
    
    if not reminders or len(reminders) > index or index < 1:
        return{
            "action" : "Update_Reminder",
            "status" : "Error",
            "message" : "Index out of the range or reminders empty in session state",
        }
    
    old_reminder = reminders[index-1]
    reminders[index-1] = new_reminder
    
    tool_context.state["reminders"] = reminders
    
    return {
        "action" : "Update_Reminders",
        "status" : "success",
        "index" : index,
        "old_reminder" : old_reminder,
        "new_reminder" : new_reminder,
        "message" : f"reminder {old_reminder}, is updated as {new_reminder}."
    }
    
    
def delete_reminder (index: int, tool_context :ToolContext) -> dict:
    """
    Delete reminder from the reminders list
    
    Args:
        index : 1 base index of the reminder to be deleted
        tool_context : context for accesing and updating the session state
        
    Return:
        confirm messages as a dictionary
    """
    
    reminders = tool_context.state.get("reminders", [])
    
    if not reminders or index < 0 or len(reminders) < index:
        return{
            "action" : "Delete_Reminder",
            "status" : "Error",
            "message" : "Invalid index or empty reminder list on state",
        }
    
    deleted_reminder = reminders.pop(index-1)
    
    tool_context.state["reminders"] = reminders
    
    return {
        "action" : "Delete_Reminder",
        "index" : index,
        "deleted_reminder" : deleted_reminder,
        "message" : f"{deleted_reminder} delete from the reminder list"
    }
    
    
def update_username (username: str, tool_context = ToolContext) -> dict:
    """Update the user name

    Args:
        username (str): new username to be updated
        tool_context: context to access and updating the session state

    Returns:
        confirm message as a dictionary
    """
    
    old_username = tool_context.state.get("username")
    tool_context.state["username"] = username 
    
    return{
        "action" : "Change_username",
        "old_username" : old_username,
        "new_username" : username,
        "message" : f"update the username and new username is {username}"
    }

Reminder_Agent = Agent(
    name="Reminder_Agent",
    model="gemini-2.0-flash",
    description="A smart reminder agent with persistent memory",
    instruction="""
    You are a friendly reminder assistant that remembers users across conversations.
    
    The user's information is stored in state:
    - User's name: {username}
    - Reminders: {reminders}
    
    You can help users manage their reminders with the following capabilities:
    1. Add new reminders
    2. View existing reminders
    3. Update reminders
    4. Delete reminders
    5. Update the user's name
    
    Always be friendly and address the user by name. If you don't know their name yet,
    use the update_user_name tool to store it when they introduce themselves.
    
    **REMINDER MANAGEMENT GUIDELINES:**
    
    When dealing with reminders, you need to be smart about finding the right reminder:
    
    1. When the user asks to update or delete a reminder but doesn't provide an index:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"), 
         look through the reminders to find a match
       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on
    
    4. For viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some
    
    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" → add_reminder("buy milk"))
    
    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which reminder the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_username,
    ],
)
