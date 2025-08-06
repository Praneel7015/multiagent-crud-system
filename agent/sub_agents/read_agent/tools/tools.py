# agent/sub_agents/read_agent/tools/tools.py

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

def read_client(client_id: int) -> Dict[str, Any]:
    """
    Retrieves a single client's details using their unique ID.

    Args:
        client_id: The unique ID of the client to find.

    Returns:
        A dictionary containing the client's data or an error message if not found.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        conn.close()
        
        if client:
            return {
                "status": "Success", 
                "message": f"Client found with ID {client_id}.",
                "client": dict(client)
            }
        return {"status": "Not Found", "message": f"Client with ID {client_id} was not found."}
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to read client: {str(e)}"}

def list_all_clients() -> Dict[str, Any]:
    """
    Retrieves a list of all clients in the database.

    Returns:
        A dictionary containing a list of all clients or an empty list if no clients exist.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY name")
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Found {len(clients)} clients in the database.",
            "clients": clients,
            "count": len(clients)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to list clients: {str(e)}"}

def list_clients_by_status(client_status: str) -> Dict[str, Any]:
    """
    Retrieves a list of clients filtered by their status (current or previous).
    
    Args:
        client_status: The status to filter by ('current' or 'previous').
    
    Returns:
        A dictionary containing matching clients.
    """
    try:
        if client_status.lower() not in ['current', 'previous']:
            return {"status": "Error", "message": "Client status must be 'current' or 'previous'"}
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE client_status = ? ORDER BY name", (client_status.lower(),))
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Found {len(clients)} {client_status} clients.",
            "clients": clients,
            "client_status": client_status,
            "count": len(clients)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to list {client_status} clients: {str(e)}"}

def search_clients_by_name(name_query: str) -> Dict[str, Any]:
    """
    Searches for clients whose names contain the given query string.
    
    Args:
        name_query: The name or partial name to search for.
    
    Returns:
        A dictionary containing matching clients.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name LIKE ? ORDER BY name", (f"%{name_query}%",))
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Found {len(clients)} clients matching '{name_query}'.",
            "clients": clients,
            "search_query": name_query,
            "count": len(clients)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to search clients: {str(e)}"}

def search_clients_by_email(email_query: str) -> Dict[str, Any]:
    """
    Searches for clients whose emails contain the given query string.
    
    Args:
        email_query: The email or partial email to search for.
    
    Returns:
        A dictionary containing matching clients.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE email LIKE ? ORDER BY email", (f"%{email_query}%",))
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Found {len(clients)} clients with email matching '{email_query}'.",
            "clients": clients,
            "search_query": email_query,
            "count": len(clients)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to search clients by email: {str(e)}"}

def get_client_statistics() -> Dict[str, Any]:
    """
    Gets detailed statistics about clients in the database.
    
    Returns:
        A dictionary with client statistics.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total count
        cursor.execute("SELECT COUNT(*) as count FROM clients")
        total_count = cursor.fetchone()["count"]
        
        # Count by status
        cursor.execute("SELECT client_status, COUNT(*) as count FROM clients GROUP BY client_status")
        status_counts = {row["client_status"]: row["count"] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client database statistics: {total_count} total clients.",
            "total_clients": total_count,
            "current_clients": status_counts.get("current", 0),
            "previous_clients": status_counts.get("previous", 0)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to get client statistics: {str(e)}"}

def display_clients_table() -> Dict[str, Any]:
    """
    Retrieves all clients and formats them in a tabular display format.
    This is perfect for showing the entire client database in an organized table.
    
    Returns:
        A dictionary containing all clients formatted as a table.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY name")
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not clients:
            return {
                "status": "Success",
                "message": "No clients found in the database.",
                "table": "| No clients to display |\n|----------------------|",
                "clients": [],
                "count": 0
            }
        
        # Create table header
        header = "| ID | Name | Address | Phone | Email | Status | Notes |\n"
        separator = "|----|----- |---------|-------|-------|--------|-------|\n"
        
        # Create table rows
        rows = []
        for client in clients:
            # Truncate long fields for better display
            name = (client['name'][:20] + '...') if len(client['name']) > 20 else client['name']
            address = (client['address'][:25] + '...') if len(client['address']) > 25 else client['address']
            phone = client['phone'] if client['phone'] else 'N/A'
            email = (client['email'][:20] + '...') if client['email'] and len(client['email']) > 20 else (client['email'] or 'N/A')
            notes = (client['notes'][:15] + '...') if client['notes'] and len(client['notes']) > 15 else (client['notes'] or 'N/A')
            status = client['client_status'].title()
            
            row = f"| {client['id']} | {name} | {address} | {phone} | {email} | {status} | {notes} |\n"
            rows.append(row)
        
        # Combine table parts
        table = header + separator + ''.join(rows)
        
        return {
            "status": "Success",
            "message": f"Client Database - Complete Table View ({len(clients)} clients)",
            "table": table,
            "clients": clients,
            "count": len(clients),
            "current_clients": len([c for c in clients if c['client_status'] == 'current']),
            "previous_clients": len([c for c in clients if c['client_status'] == 'previous'])
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to display clients table: {str(e)}"}
