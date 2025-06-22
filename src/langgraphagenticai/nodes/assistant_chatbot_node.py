import os
from dotenv import load_dotenv
from src.langgraphagenticai.state.state import State
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
import asyncio #asyncio is a library for asynchronous programming in Python.
load_dotenv()

class AgenticAIChatbotNode:
    """
    Complex agentic AI chatbot implementation
    """
    def __init__(self,model):
        self.llm=model

    def agent_node(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": "Agent"}

    def store_node(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": "Stored"}
    
    def retrieve_node(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": "Retrieved"}
    
    def email_node(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": "Email"}
    
    def calender_node(self,state:State)->dict:  
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": "Calender"}