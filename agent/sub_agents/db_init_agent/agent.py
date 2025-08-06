# agent/sub_agents/db_init_agent/agent.py

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# Import the database initialization tools
from .tools import tools

# Load environment variables from .env file
load_dotenv()

# Check for Google API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Define the database initialization agent
db_init_agent = Agent(
    name="db_init_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a database initialization specialist agent working under the Client Database Manager Agent.
    Your responsibilities include:
    - Initializing the database by creating necessary tables
    - Populating the database with sample data when needed
    - Checking database status and health
    - Ensuring the database is ready for CRUD operations
    
    🔄 WORKFLOW:
    1. Check current database status first
    2. Create tables if needed
    3. Add sample data if database is empty (optional)
    4. Confirm database readiness for operations
    5. ALWAYS end with: "Database setup complete! You're now back with the Manager Agent. What else would you like to do?"
    
    🗣️ COMMUNICATION:
    - Always check status before making changes
    - Explain what actions are being taken and why
    - Provide clear feedback about database state
    - **CRITICAL**: When calling tools, include the results in your response
    - Show actual numbers (client counts, table status) from tool responses
    - Confirm successful operations with details
    - Always return the user to the Manager Agent when done
    
    IMPORTANT: After completing database operations, always remind the user they're back with the Manager Agent for any other requests.
    """,
    tools=[
        FunctionTool(tools.initialize_database),
        FunctionTool(tools.populate_sample_data),
        FunctionTool(tools.check_database_status)
    ]
)

# Export the agent
root_agent = db_init_agent
