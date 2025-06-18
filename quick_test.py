#!/usr/bin/env python3
"""
Quick test to verify chat history functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.langgraphagenticai.LLMS.groqllm import GroqLLM

load_dotenv()

def quick_test():
    """Quick test of chat history functionality."""
    print("=== Quick Chat History Test ===")
    
    user_controls_input = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        "selected_groq_model": "gemma2-9b-it"
    }
    
    if not user_controls_input["GROQ_API_KEY"]:
        print("GROQ_API_KEY not found in environment variables.")
        return
    
    try:
        groq_llm = GroqLLM(user_contols_input=user_controls_input)
        session_id = "test_session"
        
        print("Step 1: Introducing name...")
        response1 = groq_llm.chat_with_history("My name is Shibin", session_id)
        print(f"Response 1: {response1}")

        # Debug history after first message
        groq_llm.debug_chat_history(session_id)

        print("\nStep 2: Asking about name...")
        response2 = groq_llm.chat_with_history("Do you remember my name?", session_id)
        print(f"Response 2: {response2}")

        # Debug history after second message
        groq_llm.debug_chat_history(session_id)

        # Check if the LLM actually remembered the name
        if "shibin" in response2.lower():
            print("✅ SUCCESS: Chat history is working! The LLM remembered the name.")
        else:
            print("❌ ISSUE: Chat history might not be working properly.")
            print("The LLM should have remembered 'Shibin' but didn't mention it in the response.")
        
        print("\nTest completed!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
