import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import dotenv
dotenv.load_dotenv()

class GroqLLM:
    def __init__(self, user_contols_input):
        self.user_controls_input = user_contols_input
        self.store = {}
        self.session_id = "default_session"  # Default session ID

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def add_message_to_history(self, session_id: str, role: str, content: str):
        """Manually add a message to the chat history."""
        history = self.get_session_history(session_id)
        if role == "user":
            history.add_user_message(content)
        elif role == "assistant":
            history.add_ai_message(content)
        elif role == "system":
            history.add_message(AIMessage(content=content, additional_kwargs={"role": "system"}))

    def get_chat_history(self, session_id: str = None):
        """Get the current chat history for a session."""
        if session_id is None:
            session_id = self.session_id
        history = self.get_session_history(session_id)
        return history.messages

    def clear_chat_history(self, session_id: str = None):
        """Clear chat history for a session."""
        if session_id is None:
            session_id = self.session_id
        if session_id in self.store:
            self.store[session_id] = ChatMessageHistory()

    def get_llm_model(self, session_id: str = None):
        """Get the LLM model with chat history support."""
        try:
            groq_api_key = self.user_controls_input["GROQ_API_KEY"]
            selected_groq_model = self.user_controls_input["selected_groq_model"]

            if groq_api_key == '' and os.environ.get("GROQ_API_KEY", "") == '':
                st.error("Please Enter the Groq API KEY")
                return None

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)

            # Create RunnableWithMessageHistory with proper configuration
            llm_with_history = RunnableWithMessageHistory(
                llm,
                self.get_session_history,
            )

            return llm_with_history

        except Exception as e:
            raise ValueError(f"Error Occurred With Exception: {e}")

    def chat_with_history(self, message: str = None, session_id: str = None):
        """Send a message and get response with automatic history management."""
        if session_id is None:
            session_id = self.session_id

        # If no message provided, just return the configured LLM model
        if message is None:
            return self.get_llm_model()

        llm_with_history = self.get_llm_model()

        # Get response from LLM (RunnableWithMessageHistory will automatically manage history)
        # For ChatGroq, we need to pass the message as a string directly
        response = llm_with_history.invoke(
            message,
            config={"configurable": {"session_id": session_id}}
        )

        return response.content

    def get_base_llm(self):
        """Return the base ChatGroq LLM instance (without history wrapper)."""
        groq_api_key = self.user_controls_input["GROQ_API_KEY"]
        selected_groq_model = self.user_controls_input["selected_groq_model"]
        return ChatGroq(api_key=groq_api_key, model=selected_groq_model)

if __name__ == "__main__":
    # Example usage
    user_controls_input = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        "selected_groq_model": "Gemma2-9b-It"
    }

    groq_llm = GroqLLM(user_controls_input)
    
    # Method 1: Use the chat_with_history method (recommended)
    response1 = groq_llm.chat_with_history("Hello, what's the capital of France?")
    print("Response 1:", response1)
    
    response2 = groq_llm.chat_with_history("What did I ask you before?")
    print("Response 2:", response2)  # This will remember the previous question
    
    ## Method 2: Get LLM model and use it directly
    #llm = groq_llm.get_llm_model("session_1")
    #response3 = llm.invoke("Hello again!")
    #print("Response 3:", response3.content)
    #
    ## Method 3: Manually manage history
    #groq_llm.add_message_to_history("session_2", "user", "What is 2+2?")
    #groq_llm.add_message_to_history("session_2", "assistant", "2+2 equals 4.")
    #
    #llm2 = groq_llm.get_llm_model("session_2")
    #response4 = llm2.invoke("What was the previous question?")
    #print("Response 4:", response4.content)