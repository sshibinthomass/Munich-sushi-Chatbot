import os
import streamlit as st
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()

class OpenAILLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            openai_api_key = self.user_controls_input.get("OPENAI_API_KEY", "")
            selected_openai_model = self.user_controls_input.get("selected_openai_model", "gpt-3.5-turbo")
            if openai_api_key == '' and os.environ.get("OPENAI_API_KEY", "") == '':
                st.error("Please Enter the OpenAI API KEY")
            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)
        except Exception as e:
            raise ValueError(f"Error Occurred With Exception : {e}")
        return llm

if __name__ == "__main__":
    # Example user_controls_input
    user_controls_input = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "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"),  # Use env var or set your key here
        "selected_openai_model": "gpt-4.1-mini"  # Replace with a valid model for your OpenAI account
    }

    openai_llm = OpenAILLM(user_controls_input)
    llm = openai_llm.get_llm_model()
    print(type(llm))
    if llm:
        prompt = "What is the capital of Germany?"
        try:
            response = llm.invoke(prompt)
            print("Response:", response)
        except Exception as e:
            print("Error during invocation:", e)
    else:
        print("LLM could not be initialized.")