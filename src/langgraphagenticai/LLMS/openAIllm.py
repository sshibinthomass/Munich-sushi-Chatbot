import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
import dotenv
dotenv.load_dotenv()

class OpenAILLM:
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
        """Return the base ChatOpenAI LLM instance """
        openai_api_key = self.user_controls_input.get("OPENAI_API_KEY", "")
        selected_openai_model = self.user_controls_input.get("selected_openai_model", "gpt-4.1-mini")
        return ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)


if __name__ == "__main__":
    # Example user_controls_input
    user_controls_input = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),  # Use env var or set your key here
        "selected_openai_model": "gpt-4.1-mini"  # Replace with a valid model for your OpenAI account
    }

    # openai_llm = OpenAILLM(user_controls_input)
    # llm = openai_llm.get_llm_model()
    # print(type(llm))
    # if llm:
    #     prompt = "What is the capital of Germany?"
    #     try:
    #         response = llm.invoke(prompt)
    #         print("Response:", response)
    #     except Exception as e:
    #         print("Error during invocation:", e)
    # else:
    #     print("LLM could not be initialized.")