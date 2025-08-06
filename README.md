# MultiAgent CRUD System

This project is a **conversational client management system** built with the Google Agent Development Kit (ADK). It features a natural language interface where users can interact with a friendly Manager Agent that coordinates specialized sub-agents to handle client database operations using the Gemini 2.0 Flash model.

## Key Features

- **Natural Conversation Interface** - Talk to the system in plain English
- **Intelligent Manager Agent** - Handles greetings, questions, and guidance directly
- **Smart Task Delegation** - Automatically routes specific operations to specialist agents
- **Complete Client Management** - Create, Read, Update, Delete operations for client data
- **SQLite Database** - Automatic initialization with sample data
- **Client Status Tracking** - Manage current vs previous clients
- **Formatted Table Display** - Beautiful client data presentation
- **Conversational Flow** - Sub-agents return you to the Manager for continued interaction

## Conversation Examples

```
You: "Hi"
Manager: "Hello! I'm your Client Database Manager Agent. I help you manage 
         your business clients efficiently. I can show you all your clients, 
         add new ones, update information, or remove clients you no longer need. 
         What would you like to do today?"

You: "Show me my clients"
Manager: "I'll have my Read Agent display all your clients in a nice table format."
Read Agent: [Displays formatted client table]
Read Agent: "Here's your client information! You're now back with the Manager Agent. 
            What else would you like to do?"

You: "Add a new client"
Manager: "I'll connect you with my Create Agent to add a new client."
Create Agent: [Guides through client creation process]
Create Agent: "Your new client has been added! You're now back with the Manager Agent. 
              What else would you like to do?"
```

## File Structure

```
multiagent-crud-system/
├── .env                          # Environment variables (not committed)
├── .gitignore
├── LICENSE
├── main.py                       # ADK entry point
├── README.md
├── requirements.txt
├── clients.db                    # SQLite database (auto-created)
└── agent/                        # Main agent system
    ├── __init__.py
    ├── agent.py                  # Main orchestrator agent
    └── sub_agents/               # Specialized CRUD sub-agents
        ├── db_init_agent/        # Database initialization and health checks
        ├── create_agent/         # Client creation with validation
        ├── read_agent/           # Client retrieval and table display
        ├── update_agent/         # Client modification operations
        └── delete_agent/         # Safe client deletion operations
```

## Architecture Overview

The system uses a **conversational multi-agent architecture** designed for natural interaction:

### Manager Agent (Your Main Interface)
- **Primary Role**: Handle all conversation, greetings, and general questions
- **Personality**: Friendly, helpful, and conversational 
- **Smart Delegation**: Only involves specialists for specific client operations
- **Always Available**: Maintains conversation flow and context

### Specialist Sub-Agents
- **Database Initialization Agent** - Sets up and maintains the database
- **Create Agent** - Guides users through adding new clients  
- **Read Agent** - Finds and displays client information in beautiful tables
- **Update Agent** - Modifies existing client details
- **Delete Agent** - Safely removes clients with confirmation

### Conversational Flow
```
1. You start a conversation with the Manager Agent
2. Manager handles questions, help, and guidance directly
3. For specific client operations, Manager connects you with the right specialist
4. Specialist completes the task and returns you to the Manager
5. Manager continues the conversation and asks what else you need
```

### Client Database Schema
```
clients table:
├── id (auto-generated)           # Unique identifier
├── name* (required)              # Client name
├── address* (required)           # Client address  
├── phone (optional)              # Phone number
├── email (optional)              # Email address
├── notes (optional)              # Additional information
└── client_status* (required)     # 'current' or 'previous'
```

## Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/Praneel7015/multiagent-crud-system.git
cd multiagent-crud-system
```

2. **Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

5. **Start the Conversational Interface**
```bash
python -m adk web
```

Then access the application at the provided URL (typically http://localhost:8080) and start chatting!

## How to Use

### Natural Conversation Approach
Just talk to the system naturally! Here are some examples:

**Getting Started:**
```
You: "Hi"
System: [Friendly introduction and asks what you need]

You: "What can you do?"
System: [Explains all capabilities and asks how to help]
```

**Viewing Clients:**
```
"Show me my clients"
"List all current clients" 
"Display previous clients only"
"Find clients named Sarah"
"Search for clients with gmail addresses"
```

**Managing Clients:**
```
"Add a new client named John Smith in New York"
"Create a client: Sarah Johnson, previous client, phone 555-0123"
"Update John's email address"
"Change client 5's status to previous"
"Delete the client named Mike Wilson"
```

**System Operations:**
```
"How many clients do I have?"
"Initialize the database"
"What's the system status?"
"Help me understand what I can do"
```

### Conversation Flow
1. **Start with any greeting** - The Manager Agent will introduce the system
2. **Ask questions naturally** - No need for specific commands
3. **Get connected to specialists** - For specific operations, you'll be transferred to the right expert
4. **Return to Manager** - After each task, you're back with the main Agent for more questions

## Database Schema

```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    notes TEXT,
    client_status TEXT NOT NULL CHECK(client_status IN ('current', 'previous'))
````
);
```

## Technical Details

- **Framework**: Google Agent Development Kit (ADK) v0.3.0
- **AI Model**: Gemini 2.0 Flash
- **Database**: SQLite 3 with automatic initialization and sample data
- **Architecture**: Conversational Multi-Agent System with smart delegation
- **Python**: 3.8+ required
- **Interface**: Natural language web chat interface

## Agent Personalities

Each agent has its own personality and communication style:

- **Manager Agent**: Friendly, welcoming, always ready to help and guide
- **Create Agent**: Methodical, asks good questions, ensures complete information
- **Read Agent**: Organized, presents data beautifully, offers search refinements  
- **Update Agent**: Careful, shows before/after changes, validates thoroughly
- **Delete Agent**: Cautious, confirms everything, warns about permanent actions
- **Database Agent**: Technical, efficient, reports status clearly

## What Makes This Special

1. **True Conversational AI** - No rigid commands, just natural language
2. **Intelligent Agent Coordination** - Right specialist for each task
3. **Seamless Context Switching** - Smooth transitions between agents
4. **User-Friendly Returns** - Always guided back to the main interface
5. **Smart Delegation** - Manager handles general questions, specialists handle operations

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

