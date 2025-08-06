# agent/sub_agents/delete_agent/tools/tools.py

import sqlite3
import os
from typing import Dict, Any, List

# Database file path relative to project root
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "clients.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def delete_client(client_id: int) -> Dict[str, Any]:
    """
    Deletes a client from the database using their unique ID.

    Args:
        client_id: The unique ID of the client to delete.

    Returns:
        A dictionary with success or error message and deleted client info.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First get the client data before deletion
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client_to_delete = cursor.fetchone()
        
        if not client_to_delete:
            conn.close()
            return {"status": "Not Found", "message": f"Client with ID {client_id} not found."}
        
        # Delete the client
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client '{client_to_delete['name']}' with ID {client_id} was deleted successfully.",
            "deleted_client": dict(client_to_delete)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to delete client: {str(e)}"}

def delete_client_by_email(email: str) -> Dict[str, Any]:
    """
    Deletes a client from the database using their email address.

    Args:
        email: The email address of the client to delete.

    Returns:
        A dictionary with success or error message and deleted client info.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First get the client data before deletion
        cursor.execute("SELECT * FROM clients WHERE email = ?", (email,))
        client_to_delete = cursor.fetchone()
        
        if not client_to_delete:
            conn.close()
            return {"status": "Not Found", "message": f"Client with email '{email}' not found."}
        
        # Delete the client
        cursor.execute("DELETE FROM clients WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client '{client_to_delete['name']}' with email '{email}' was deleted successfully.",
            "deleted_client": dict(client_to_delete)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to delete client by email: {str(e)}"}

def delete_multiple_clients(client_ids: List[int]) -> Dict[str, Any]:
    """
    Deletes multiple clients from the database using their IDs.

    Args:
        client_ids: A list of client IDs to delete.

    Returns:
        A dictionary with results of the deletion operation.
    """
    if not client_ids:
        return {"status": "Error", "message": "No client IDs provided for deletion."}
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        deleted_clients = []
        not_found_ids = []
        
        for client_id in client_ids:
            # Get client data before deletion
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client_to_delete = cursor.fetchone()
            
            if client_to_delete:
                cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
                deleted_clients.append(dict(client_to_delete))
            else:
                not_found_ids.append(client_id)
        
        conn.commit()
        conn.close()
        
        result = {
            "status": "Completed",
            "message": f"Attempted to delete {len(client_ids)} clients. {len(deleted_clients)} deleted, {len(not_found_ids)} not found.",
            "deleted_clients": deleted_clients,
            "deleted_count": len(deleted_clients),
            "not_found_ids": not_found_ids
        }
        
        return result
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to delete multiple clients: {str(e)}"}

def confirm_client_exists_for_deletion(client_id: int) -> Dict[str, Any]:
    """
    Confirms that a client exists before deletion and shows their details.
    
    Args:
        client_id: The ID of the client to confirm for deletion.
    
    Returns:
        A dictionary with client details or not found message.
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
                "message": f"Client exists and ready for deletion.",
                "client": dict(client),
                "warning": "This client will be permanently deleted. This action cannot be undone."
            }
        else:
            return {"status": "Not Found", "message": f"Client with ID {client_id} does not exist."}
            
    except Exception as e:
        return {"status": "Error", "message": f"Failed to confirm client for deletion: {str(e)}"}

def clear_all_clients() -> Dict[str, Any]:
    """
    Deletes ALL clients from the database. Use with extreme caution!
    
    Returns:
        A dictionary with the result of the operation.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First count how many clients will be deleted
        cursor.execute("SELECT COUNT(*) as count FROM clients")
        count_before = cursor.fetchone()["count"]
        
        if count_before == 0:
            conn.close()
            return {"status": "Info", "message": "Database is already empty. No clients to delete."}
        
        # Delete all clients
        cursor.execute("DELETE FROM clients")
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"All {count_before} clients have been deleted from the database.",
            "deleted_count": count_before,
            "warning": "All client data has been permanently removed."
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to clear all clients: {str(e)}"}

def delete_all_previous_clients() -> Dict[str, Any]:
    """
    Deletes all clients with status 'previous' from the database.
    This is useful for cleaning up old client records.

    Returns:
        A dictionary with success or error message and count of deleted clients.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count previous clients before deletion
        cursor.execute("SELECT COUNT(*) as count FROM clients WHERE client_status = 'previous'")
        count_before = cursor.fetchone()["count"]
        
        if count_before == 0:
            conn.close()
            return {"status": "Info", "message": "No previous clients found to delete."}
        
        # Delete all previous clients
        cursor.execute("DELETE FROM clients WHERE client_status = 'previous'")
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"All {count_before} previous clients have been deleted from the database.",
            "deleted_count": count_before,
            "warning": "All previous client data has been permanently removed."
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to delete all previous clients: {str(e)}"}

def delete_all_current_clients() -> Dict[str, Any]:
    """
    Deletes all clients with status 'current' from the database.
    Use with caution as this removes all active client records.

    Returns:
        A dictionary with success or error message and count of deleted clients.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count current clients before deletion
        cursor.execute("SELECT COUNT(*) as count FROM clients WHERE client_status = 'current'")
        count_before = cursor.fetchone()["count"]
        
        if count_before == 0:
            conn.close()
            return {"status": "Info", "message": "No current clients found to delete."}
        
        # Delete all current clients
        cursor.execute("DELETE FROM clients WHERE client_status = 'current'")
        conn.commit()
        conn.close()
        
        return {
            "status": "Success",
            "message": f"All {count_before} current clients have been deleted from the database.",
            "deleted_count": count_before,
            "warning": "All current client data has been permanently removed."
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to delete all current clients: {str(e)}"}

