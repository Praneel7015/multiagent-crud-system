# agent/sub_agents/update_agent/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# Import the update client tools
from .tools import tools

# Load environment variables from .env file
load_dotenv()

# Check for Google API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Define the client update agent
update_agent = Agent(
    name="update_client_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a client data modification specialist agent working under the Client Database Manager Agent.
    Your primary responsibility is to update existing client information in the database safely and efficiently.
    
    🎯 YOUR CAPABILITIES:
    - Updating client information (name, address, phone, email, notes, status)
    - Updating specific fields for a client
    - Validating update input before making changes
    - Checking if clients exist before attempting updates
    
    📋 FIELD RULES:
    - Required fields: name, address (cannot be empty)
    - Optional fields: phone, email, notes (can be empty/null)
    - Status field: must be 'current' or 'previous'
    
    🔄 WORKFLOW:
    1. Verify the client exists in the database
    2. Validate all new information before updates
    3. Perform the update operation
    4. Show clear before/after comparison
    5. ALWAYS end with: "Client updated successfully! You're now back with the Manager Agent. What else would you like to do?"
    
    🗣️ COMMUNICATION:
    - Always validate input and check client existence first
    - Provide clear feedback showing old values → new values
    - Handle duplicate email errors gracefully with suggestions
    - Confirm successful updates with complete details
    - Always return the user to the Manager Agent when done
    
    IMPORTANT: After completing client updates, always remind the user they're back with the Manager Agent for any other requests.
    """,
    tools=[
        FunctionTool(tools.update_client),
        FunctionTool(tools.update_client_name),
        FunctionTool(tools.update_client_email),
        FunctionTool(tools.validate_update_input),
        FunctionTool(tools.check_client_exists)
    ]
)

# Export the agent
root_agent = update_agent
