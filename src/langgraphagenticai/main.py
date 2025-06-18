import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.openAIllm import OpenAILLM
from src.langgraphagenticai.LLMS.ollamallm import OllamaLLMWrapper

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """

    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input: #This is the user input from the UI if no user input is found then error is shown
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message:") #This is the user message from the UI

    # Initialize chat history in session state if not present
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Initialize session ID for consistent chat history across LLMs
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = "streamlit_session"

    # Initialize or get existing LLM config object to maintain chat history
    current_llm = user_input["selected_llm"]

    # Check if we need to create a new LLM config (first time or LLM changed)
    if ('llm_config' not in st.session_state or
        'current_llm_type' not in st.session_state or
        st.session_state['current_llm_type'] != current_llm):

        try:
            ## Configure The LLM's with chat history support
            if current_llm == "Groq":
                st.session_state['llm_config'] = GroqLLM(user_contols_input=user_input)
            elif current_llm == "Ollama":
                st.session_state['llm_config'] = OllamaLLMWrapper(user_controls_input=user_input)
            elif current_llm == "OpenAI":
                st.session_state['llm_config'] = OpenAILLM(user_controls_input=user_input)

            # Store the current LLM type
            st.session_state['current_llm_type'] = current_llm

            # Test if the model can be initialized
            test_model = st.session_state['llm_config'].get_llm_model(st.session_state['session_id'])
            if not test_model:
                st.error("Error: LLM model could not be initialized")
                return

        except Exception as e:
            st.error(f"Error: LLM configuration failed- {e}")
            return

    if user_message:
        try:
            # Use the persistent LLM config object for chat with history
            obj_llm_config = st.session_state['llm_config']

            # Use chat_with_history method for context-aware responses
            response = obj_llm_config.chat_with_history(user_message, st.session_state['session_id'])

            # Append user message to streamlit chat history for display
            st.session_state['chat_history'].append({"role": "user", "content": user_message})
            # Append assistant message to streamlit chat history for display
            st.session_state['chat_history'].append({"role": "assistant", "content": response})

        except Exception as e:
             st.error(f"Error: Chat processing failed- {e}")
             return

    # Display the full chat history
    for msg in st.session_state['chat_history']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Add a button to clear chat history
    if st.sidebar.button("Clear Chat History"):
        st.session_state['chat_history'] = []
        if 'llm_config' in st.session_state:
            st.session_state['llm_config'].clear_chat_history(st.session_state['session_id'])
        st.rerun()
