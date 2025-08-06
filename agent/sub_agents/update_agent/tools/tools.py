# agent/sub_agents/update_agent/tools/tools.py

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

def update_client(client_id: int, name: str = None, address: str = None, phone: Optional[str] = None, email: Optional[str] = None, notes: Optional[str] = None, client_status: str = None) -> Dict[str, Any]:
    """
    Updates client information based on their ID. Only provided fields will be updated.

    Args:
        client_id: The unique ID of the client to update.
        name: The new name for the client (required if provided).
        address: The new address for the client (required if provided).
        phone: The new phone number for the client (optional).
        email: The new email address for the client (optional).
        notes: The new notes for the client (optional).
        client_status: The new status ('current' or 'previous') for the client.

    Returns:
        A dictionary containing the updated client's data or an error message.
    """
    if not any([name, address, phone is not None, email is not None, notes is not None, client_status]):
        return {"status": "Error", "message": "At least one field must be provided to update."}
    
    if client_status and client_status.lower() not in ['current', 'previous']:
        return {"status": "Error", "message": "Client status must be 'current' or 'previous'."}
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if client exists
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        existing_client = cursor.fetchone()
        
        if not existing_client:
            conn.close()
            return {"status": "Not Found", "message": f"Client with ID {client_id} not found."}
        
        # Build update query dynamically
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if address:
            updates.append("address = ?")
            params.append(address)
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        if client_status:
            updates.append("client_status = ?")
            params.append(client_status.lower())
        
        params.append(client_id)
        
        # Update the client
        query = f"UPDATE clients SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        # Get updated client data
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        updated_client = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client with ID {client_id} updated successfully.",
            "old_client": dict(existing_client),
            "updated_client": dict(updated_client)
        }
        
    except sqlite3.IntegrityError as e:
        return {"status": "Error", "message": f"Update failed due to constraint violation: {str(e)}"}
    except Exception as e:
        return {"status": "Error", "message": f"Failed to update client: {str(e)}"}

def update_client_name(client_id: int, name: str) -> Dict[str, Any]:
    """
    Updates only the name of an existing client.

    Args:
        client_id: The unique ID of the client to update.
        name: The new name for the client.

    Returns:
        A dictionary containing the result of the update operation.
    """
    if not name or not name.strip():
        return {"status": "Error", "message": "Name cannot be empty."}
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if client exists
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        existing_client = cursor.fetchone()
        
        if not existing_client:
            conn.close()
            return {"status": "Not Found", "message": f"Client with ID {client_id} not found."}
        
        # Update the client name
        cursor.execute("UPDATE clients SET name = ? WHERE id = ?", (name, client_id))
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client name updated from '{existing_client['name']}' to '{name}'.",
            "client_id": client_id,
            "old_name": existing_client['name'],
            "new_name": name
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to update client name: {str(e)}"}

def update_client_email(client_id: int, email: Optional[str]) -> Dict[str, Any]:
    """
    Updates only the email of an existing client.

    Args:
        client_id: The unique ID of the client to update.
        email: The new email address for the client (can be None to clear email).

    Returns:
        A dictionary containing the result of the update operation.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if client exists
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        existing_client = cursor.fetchone()
        
        if not existing_client:
            conn.close()
            return {"status": "Not Found", "message": f"Client with ID {client_id} not found."}
        
        # Update the client email
        cursor.execute("UPDATE clients SET email = ? WHERE id = ?", (email, client_id))
        conn.commit()
        conn.close()
        
        old_email = existing_client['email'] or 'None'
        new_email = email or 'None'
        
        return {
            "status": "Success",
            "message": f"Client email updated from '{old_email}' to '{new_email}'.",
            "client_id": client_id,
            "old_email": existing_client['email'],
            "new_email": email
        }
        
    except sqlite3.IntegrityError as e:
        return {"status": "Error", "message": f"Email update failed - email may already exist: {str(e)}"}
    except Exception as e:
        return {"status": "Error", "message": f"Failed to update client email: {str(e)}"}

def validate_update_input(name: str = None, address: str = None, email: Optional[str] = None, client_status: str = None) -> Dict[str, Any]:
    """
    Validates input data for client updates before attempting the update.

    Args:
        name: The name to validate (optional).
        address: The address to validate (optional).
        email: The email to validate (optional).
        client_status: The client status to validate (optional).

    Returns:
        A dictionary containing validation results.
    """
    validation_errors = []
    
    if name is not None and (not name or not name.strip()):
        validation_errors.append("Name cannot be empty if provided.")
    
    if address is not None and (not address or not address.strip()):
        validation_errors.append("Address cannot be empty if provided.")
    
    if email is not None and email and '@' not in email:
        validation_errors.append("Email must contain '@' symbol if provided.")
    
    if client_status is not None and client_status.lower() not in ['current', 'previous']:
        validation_errors.append("Client status must be 'current' or 'previous'.")
    
    if validation_errors:
        return {
            "status": "Invalid",
            "message": "Validation failed.",
            "errors": validation_errors
        }
    
    return {
        "status": "Valid",
        "message": "All provided inputs are valid for update.",
        "validated_fields": {
            "name": name,
            "address": address,
            "email": email,
            "client_status": client_status
        }
    }

def check_client_exists(client_id: int) -> Dict[str, Any]:
    """
    Checks if a client exists in the database and returns their current information.

    Args:
        client_id: The ID of the client to check.

    Returns:
        A dictionary containing client information or not found message.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        
        if client:
            return {
                "status": "Found",
                "message": f"Client with ID {client_id} exists.",
                "client": dict(client)
            }
        else:
            return {"status": "Not Found", "message": f"Client with ID {client_id} does not exist."}
            
    except Exception as e:
        return {"status": "Error", "message": f"Failed to check client existence: {str(e)}"}
