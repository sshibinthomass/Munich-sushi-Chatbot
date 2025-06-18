import streamlit as st
from langchain_ollama import OllamaLLM  # Updated import as per deprecation warning
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage

class OllamaLLMWrapper:
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
            selected_ollama_model = self.user_controls_input.get("selected_ollama_model")
            ollama_base_url = self.user_controls_input.get("OLLAMA_BASE_URL", "http://localhost:11434")

            if not selected_ollama_model:
                st.error("Please select an Ollama model.")
                return None

            llm = OllamaLLM(
                model=selected_ollama_model,
                base_url=ollama_base_url
            )

            # Create RunnableWithMessageHistory with proper configuration
            llm_with_history = RunnableWithMessageHistory(
                llm,
                self.get_session_history,
            )

            return llm_with_history

        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")

    def chat_with_history(self, message: str, session_id: str = None):
        """Send a message and get response with automatic history management."""
        if session_id is None:
            session_id = self.session_id

        llm_with_history = self.get_llm_model()

        # Get response from LLM (RunnableWithMessageHistory will automatically manage history)
        # For OllamaLLM, we need to pass the message as a string directly
        response = llm_with_history.invoke(
            message,
            config={"configurable": {"session_id": session_id}}
        )

        # For Ollama, response might be a string directly
        if hasattr(response, 'content'):
            return response.content
        else:
            return response

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