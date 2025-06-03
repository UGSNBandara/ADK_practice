from google.genai import types

def disply_state(session_service, app_name, user_id, session_id, label="Current state"):
    """Display the session state in a formated way."""
    
    try:
        session = session_service.get_session(
            app_name = app_name, user_id = user_id, session_id=session_id
        )
        
        print(f"{'-' * 40}")
        print(f" - - - {label} - - - ")
        username =  session.state.get("username", "unknown")
        print(f"User : {username}")
        
        reminders = session.state.get("reminders", [])
        if reminders:
            print("Reminders list : ")
            for idx, reminder in enumerate(reminders, 1):
                print(f"{idx}. {reminder}")
        
        else:
            print("Reminders : None")
        print(f"{'-' * 40}")
        
    except Exception as e:
        print(f"An Error occured while displying state : {e}")


async def process_agent_response(event):
    """Process and display agent response event"""
    
    print(f"Event Id : {event.id}, Author: {event.author}")
    
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            
            if hasattr(part, "executable_code") and part.executable_code:
                # access the actual code string via .code 
                print(f"Debug : Agent denarated code: \n \n {part.executable_code.code}\n")
                has_specific_part = True
                
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                # to access outcome and output
                print(f"Debug : Code execution result : {part.code_execution_result.outcome}\n output: {part.code_execution_result.output}")
                has_specific_part = True
            
            elif hasattr(part, "tool_response") and part.tool_response:
                #print tool response imformations
                print(f"Tool response: {part.tool_response.output}")
                has_specific_part = True

            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"Text: '{part.text.strip()}")
                #text found in any parts for debugging
            
        final_response = None
        if event.is_final_response():
            if (
                event.content 
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text
            ):
                final_response = event.content.parts[0].text.strip()
                print(f"{'- ' * 40}")
                print(f"Agent Response : - \n {final_response}")
                
                
            else:
                ##print no text xontent in final event
                print("No text content in final event")
            
    return final_response

async def call_agent_async(runner, user_id, session_id, query):
    """ Call the agent asyncronusly with user's query"""
    
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print(f"Running Query : {query}")
    
    final_response_text = None
    
    #display state before processing
    disply_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State before Processing",
    )
    
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during the agent call : {e}")
    
    disply_state(
        runner.session_service,
        runner.app_name, 
        user_id,
        session_id,
        "Satate after processing"
    )
    
    return final_response_text