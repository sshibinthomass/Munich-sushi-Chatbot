import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
import dotenv
dotenv.load_dotenv()

class OpenAILLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
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
            openai_api_key = self.user_controls_input.get("OPENAI_API_KEY", "")
            selected_openai_model = self.user_controls_input.get("selected_openai_model", "gpt-4.1-mini")

            if openai_api_key == '' and os.environ.get("OPENAI_API_KEY", "") == '':
                st.error("Please Enter the OpenAI API KEY")
                return None

            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)

            # Create RunnableWithMessageHistory with proper configuration
            llm_with_history = RunnableWithMessageHistory(
                llm,
                self.get_session_history,
            )

            return llm_with_history

        except Exception as e:
            raise ValueError(f"Error Occurred With Exception : {e}")

    def get_base_llm(self):
        """Return the base ChatOpenAI LLM instance (without history wrapper)."""
        openai_api_key = self.user_controls_input.get("OPENAI_API_KEY", "")
        selected_openai_model = self.user_controls_input.get("selected_openai_model", "gpt-4.1-mini")
        return ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)

    def chat_with_history(self, message: str, session_id: str = None):
        """Send a message and get response with automatic history management."""
        if session_id is None:
            session_id = self.session_id

        llm_with_history = self.get_llm_model()

        # Get response from LLM (RunnableWithMessageHistory will automatically manage history)
        # For ChatOpenAI, we need to pass the message as a string directly
        response = llm_with_history.invoke(
            message,
            config={"configurable": {"session_id": session_id}}
        )

        return response.content

if __name__ == "__main__":
    # Example user_controls_input
    user_controls_input = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),  # Use env var or set your key here
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