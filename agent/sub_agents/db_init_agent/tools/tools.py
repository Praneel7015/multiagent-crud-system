# agent/sub_agents/db_init_agent/tools/tools.py

import sqlite3
import os
from typing import Dict, Any

# Database file path relative to project root
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "clients.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Creates the 'clients' table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            notes TEXT,
            client_status TEXT NOT NULL CHECK(client_status IN ('current', 'previous'))
        )
    """)
    conn.commit()
    conn.close()

def initialize_database() -> Dict[str, Any]:
    """
    Initializes the database by creating the clients table if it doesn't exist.
    
    Returns:
        A dictionary indicating success or failure of the database initialization.
    """
    try:
        create_table()
        return {"status": "Success", "message": "Client database initialized successfully."}
    except Exception as e:
        return {"status": "Error", "message": f"Failed to initialize database: {str(e)}"}

def populate_sample_data() -> Dict[str, Any]:
    """
    Populates the database with sample client data if it's empty.
    
    Returns:
        A dictionary indicating success or failure of data population.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) as count FROM clients")
        count = cursor.fetchone()["count"]
        
        if count > 0:
            conn.close()
            return {"status": "Info", "message": f"Database already contains {count} clients. No sample data added."}
        
        # Add sample clients
        sample_clients = [
            ("Alice Smith", "123 Main St, New York, NY", "555-0101", "alice@example.com", "Long-term client, prefers email communication", "current"),
            ("Bob Johnson", "456 Oak Ave, Los Angeles, CA", "555-0102", "bob@example.com", "New client, referred by Alice", "current"),
            ("Charlie Lee", "789 Pine Rd, Chicago, IL", "555-0103", "charlie@example.com", "Completed project successfully", "previous"),
            ("Dana White", "321 Elm St, Houston, TX", "555-0104", "dana@example.com", "High-priority client", "current"),
            ("Eve Black", "654 Maple Dr, Phoenix, AZ", "555-0105", "eve@example.com", "Contract ended last year", "previous")
        ]
        
        cursor.executemany("INSERT INTO clients (name, address, phone, email, notes, client_status) VALUES (?, ?, ?, ?, ?, ?)", sample_clients)
        conn.commit()
        conn.close()
        
        return {
            "status": "Success", 
            "message": f"Successfully added {len(sample_clients)} sample clients to the database.",
            "clients_added": len(sample_clients)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to populate sample data: {str(e)}"}

def check_database_status() -> Dict[str, Any]:
    """
    Checks the current status of the database including table existence and client count.
    
    Returns:
        A dictionary with database status information.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if clients table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            conn.close()
            return {
                "status": "Warning",
                "message": "Clients table does not exist.",
                "table_exists": False,
                "client_count": 0
            }
        
        # Count clients
        cursor.execute("SELECT COUNT(*) as count FROM clients")
        client_count = cursor.fetchone()["count"]
        
        # Count by status
        cursor.execute("SELECT client_status, COUNT(*) as count FROM clients GROUP BY client_status")
        status_counts = {row["client_status"]: row["count"] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "status": "Success",
            "message": f"Client database is ready. Clients table exists with {client_count} clients.",
            "table_exists": True,
            "client_count": client_count,
            "current_clients": status_counts.get("current", 0),
            "previous_clients": status_counts.get("previous", 0)
        }
        
    except Exception as e:
        return {"status": "Error", "message": f"Failed to check database status: {str(e)}"}
