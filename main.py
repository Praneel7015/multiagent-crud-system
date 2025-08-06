# main.py

"""
Main entry point for the Google ADK Database Agent.
This file exposes the root agent for the ADK framework.
"""

from agent import root_agent

# Export the root agent for ADK to discover
__all__ = ["root_agent"]
