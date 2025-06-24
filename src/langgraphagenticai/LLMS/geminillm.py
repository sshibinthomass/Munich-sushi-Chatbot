import os
# Replace this import with the actual Gemini LLM class you use
# For example, if using langchain_google_genai:
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
import dotenv
dotenv.load_dotenv()

class GeminiLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
        self.store = {}
        self.session_id = "default_session"  # Default session ID

    def clear_chat_history(self, session_id: str = None):
        """Clear chat history for a session."""
        if session_id is None:
            session_id = self.session_id
        if session_id in self.store:
            self.store[session_id] = ChatMessageHistory()

    def get_base_llm(self):
        """Return the base Gemini LLM instance"""
        gemini_api_key = self.user_controls_input["GEMINI_API_KEY"]
        selected_gemini_model = self.user_controls_input["selected_gemini_model"]
        return ChatGoogleGenerativeAI(api_key=gemini_api_key, model=selected_gemini_model)

if __name__ == "__main__":
    # Example usage
    user_controls_input = {
        "GEMINI_API_KEY": "",
        "selected_gemini_model": "gemini-2.5-flash"
    }

    gemini_llm = GeminiLLM(user_controls_input)
    llm = gemini_llm.get_base_llm()

    # Simple test prompt
    prompt = "Hello, who won the FIFA World Cup in 2018?"
    try:
        # The method to call may differ depending on the LLM class.
        # For langchain's ChatGoogleGenerativeAI, you typically use .invoke() or .predict()
        response = llm.invoke(prompt)
        print(response)
    except Exception as e:
        print("Error during LLM invocation:", e)
