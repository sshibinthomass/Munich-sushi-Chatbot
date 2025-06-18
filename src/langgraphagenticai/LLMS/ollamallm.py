import os
import streamlit as st
from langchain_ollama import OllamaLLM  # Updated import as per deprecation warning

class OllamaLLMWrapper:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            selected_ollama_model = self.user_controls_input.get("selected_ollama_model")
            ollama_base_url = self.user_controls_input.get("OLLAMA_BASE_URL", "http://localhost:11434")
            if not selected_ollama_model:
                st.error("Please select an Ollama model.")
                return None
            llm = OllamaLLM(
                model=selected_ollama_model,
                base_url=ollama_base_url
            )
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
        return llm

if __name__ == "__main__":
    user_controls_input = {
        "selected_ollama_model": "llama2",  # Replace with a model available on your Ollama server
        "OLLAMA_BASE_URL": "http://localhost:11434"
    }

    ollama_llm = OllamaLLMWrapper(user_controls_input)
    llm = ollama_llm.get_llm_model()
    #print(type(llm))
    if llm:
        prompt = "Hello, what is the capital of germany?"
        try:
            response = llm.invoke(prompt)
            print("Response:", response)
        except Exception as e:
            print("Error during invocation:", e)
    else:
        print("LLM could not be initialized.")