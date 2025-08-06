# agent/sub_agents/create_agent/tools/tools.py

import sqlite3
import os
from typing import Dict, Any, Optional

# Database file path relative to project root
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "clients.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_client(name: str, address: str, client_status: str, phone: Optional[str] = None, email: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new client in the database. Use this when asked to add or create a new client.
    Name and address are mandatory, phone, email, and notes are optional.

    Args:
        name: The full name of the client (required).
        address: The full address of the client (required).
        client_status: Whether this is a 'current' or 'previous' client (required).
        phone: The phone number of the client (optional).
        email: The email address of the client (optional).
        notes: Additional notes about the client (optional).

    Returns:
        A dictionary containing the details of the newly created client or an error.
    """
    try:
        # Validate required fields
        validation = validate_client_input(name, address, client_status)
        if validation["status"] != "Valid":
            return validation
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (name, address, phone, email, notes, client_status) VALUES (?, ?, ?, ?, ?, ?)", 
            (name, address, phone, email, notes, client_status)
        )
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()
        
        return {
            "status": "Success", 
            "message": f"Client '{name}' created successfully as a {client_status} client.",
            "client": {
                "id": client_id, 
                "name": name, 
                "address": address,
                "phone": phone,
                "email": email,
                "notes": notes,
                "client_status": client_status
            }
        }
    except sqlite3.IntegrityError as e:
        return {"status": "Error", "message": f"Failed to create client due to data conflict: {str(e)}"}
    except Exception as e:
        return {"status": "Error", "message": f"Failed to create client: {str(e)}"}

def validate_client_input(name: str, address: str, client_status: str) -> Dict[str, Any]:
    """
    Validates client input before creating a client.
    
    Args:
        name: The name to validate (required).
        address: The address to validate (required).
        client_status: The client status to validate (required).
    
    Returns:
        A dictionary indicating if the input is valid or what errors exist.
    """
    errors = []
    
    if not name or not name.strip():
        errors.append("Name cannot be empty")
    elif len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    if not address or not address.strip():
        errors.append("Address cannot be empty")
    elif len(address.strip()) < 5:
        errors.append("Address must be at least 5 characters long")
        
    if not client_status or client_status.lower() not in ['current', 'previous']:
        errors.append("Client status must be either 'current' or 'previous'")
    
    if errors:
        return {"status": "Invalid", "errors": errors}
    
    return {"status": "Valid", "message": "Input validation passed"}

def validate_email_format(email: str) -> Dict[str, Any]:
    """
    Validates email format if provided.
    
    Args:
        email: The email address to validate.
    
    Returns:
        A dictionary indicating if the email format is valid.
    """
    if not email:
        return {"status": "Valid", "message": "No email provided (optional field)"}
        
    if "@" not in email or "." not in email or len(email) < 5:
        return {"status": "Invalid", "message": "Email must be in a valid format (example@domain.com)"}
    
    return {"status": "Valid", "message": "Email format is valid"}
