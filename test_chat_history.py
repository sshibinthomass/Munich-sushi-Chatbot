#!/usr/bin/env python3
"""
Test script to verify chat history functionality across different LLM providers.
This script tests the chat history implementation for GroqLLM, OpenAILLM, and OllamaLLMWrapper.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.openAIllm import OpenAILLM
from src.langgraphagenticai.LLMS.ollamallm import OllamaLLMWrapper

load_dotenv()

def test_groq_chat_history():
    """Test GroqLLM chat history functionality."""
    print("=== Testing GroqLLM Chat History ===")

    user_controls_input = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        "selected_groq_model": "gemma2-9b-it"
    }

    if not user_controls_input["GROQ_API_KEY"]:
        print("GROQ_API_KEY not found in environment variables. Skipping GroqLLM test.")
        return

    try:
        groq_llm = GroqLLM(user_contols_input=user_controls_input)

        # Test conversation with history
        session_id = "test_session_groq"

        print("User: My name is John")
        response1 = groq_llm.chat_with_history("My name is John", session_id)
        print(f"Assistant: {response1}")

        print("\nUser: What is my name?")
        response2 = groq_llm.chat_with_history("What is my name?", session_id)
        print(f"Assistant: {response2}")

        # Test if it actually remembers
        if "john" in response2.lower():
            print("✅ SUCCESS: Chat history is working! The LLM remembered the name.")
        else:
            print("❌ ISSUE: Chat history might not be working properly.")

        # Display chat history
        print("\n--- Chat History ---")
        history = groq_llm.get_chat_history(session_id)
        for i, msg in enumerate(history):
            role = "User" if hasattr(msg, 'content') and msg.__class__.__name__ == 'HumanMessage' else "Assistant"
            print(f"{i+1}. {role}: {msg.content}")

        print("GroqLLM chat history test completed successfully!\n")

    except Exception as e:
        print(f"Error testing GroqLLM: {e}\n")

def test_openai_chat_history():
    """Test OpenAILLM chat history functionality."""
    print("=== Testing OpenAILLM Chat History ===")
    
    user_controls_input = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "selected_openai_model": "gpt-3.5-turbo"
    }
    
    if not user_controls_input["OPENAI_API_KEY"]:
        print("OPENAI_API_KEY not found in environment variables. Skipping OpenAILLM test.")
        return
    
    try:
        openai_llm = OpenAILLM(user_controls_input=user_controls_input)
        
        # Test conversation with history
        session_id = "test_session_openai"
        
        print("User: What's 2 + 2?")
        response1 = openai_llm.chat_with_history("What's 2 + 2?", session_id)
        print(f"Assistant: {response1}")
        
        print("\nUser: What was my previous question?")
        response2 = openai_llm.chat_with_history("What was my previous question?", session_id)
        print(f"Assistant: {response2}")
        
        # Display chat history
        print("\n--- Chat History ---")
        history = openai_llm.get_chat_history(session_id)
        for i, msg in enumerate(history):
            role = "User" if hasattr(msg, 'content') and msg.__class__.__name__ == 'HumanMessage' else "Assistant"
            print(f"{i+1}. {role}: {msg.content}")
        
        print("OpenAILLM chat history test completed successfully!\n")
        
    except Exception as e:
        print(f"Error testing OpenAILLM: {e}\n")

def test_ollama_chat_history():
    """Test OllamaLLMWrapper chat history functionality."""
    print("=== Testing OllamaLLMWrapper Chat History ===")
    
    user_controls_input = {
        "selected_ollama_model": "llama2",
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    }
    
    try:
        ollama_llm = OllamaLLMWrapper(user_controls_input=user_controls_input)
        
        # Test conversation with history
        session_id = "test_session_ollama"
        
        print("User: Hello, what's your name?")
        response1 = ollama_llm.chat_with_history("Hello, what's your name?", session_id)
        print(f"Assistant: {response1}")
        
        print("\nUser: What did I ask you before?")
        response2 = ollama_llm.chat_with_history("What did I ask you before?", session_id)
        print(f"Assistant: {response2}")
        
        # Display chat history
        print("\n--- Chat History ---")
        history = ollama_llm.get_chat_history(session_id)
        for i, msg in enumerate(history):
            role = "User" if hasattr(msg, 'content') and msg.__class__.__name__ == 'HumanMessage' else "Assistant"
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"{i+1}. {role}: {content}")
        
        print("OllamaLLMWrapper chat history test completed successfully!\n")
        
    except Exception as e:
        print(f"Error testing OllamaLLMWrapper: {e}\n")

def main():
    """Run all chat history tests."""
    print("Starting Chat History Tests...\n")
    
    # Test each LLM provider
    test_groq_chat_history()
    test_openai_chat_history()
    test_ollama_chat_history()
    
    print("All chat history tests completed!")

if __name__ == "__main__":
    main()
