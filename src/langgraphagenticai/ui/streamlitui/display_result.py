import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, graph, user_message, selected_llm=None, chat_history=None, session_id=None):
        self.graph = graph
        self.user_message = user_message
        self.selected_llm = selected_llm
        self.chat_history = chat_history or []
        self.session_id = session_id or "default_session"

    def display_result_on_ui(self):
        """Display the conversation result on the UI with chat history context."""
        graph = self.graph
        user_message = self.user_message
        selected_llm = self.selected_llm

        # Create messages with chat history context
        messages_input = self._prepare_messages_with_history()

        for event in graph.stream({'messages': messages_input}):
            for value in event.values():
                with st.chat_message("user"):
                    st.write(user_message)
                with st.chat_message("assistant"):
                    if selected_llm == "Groq" or selected_llm == "OpenAI":
                        st.write(value["messages"].content)
                    else:
                        st.write(value["messages"])

    def get_assistant_response(self):
        """Get assistant response with chat history context."""
        graph = self.graph
        selected_llm = self.selected_llm

        # Create messages with chat history context
        messages_input = self._prepare_messages_with_history()

        for event in graph.stream({'messages': messages_input}):
            for value in event.values():
                if selected_llm == "Groq" or selected_llm == "OpenAI":
                    return value["messages"].content
                else:
                    return value["messages"]

    def _prepare_messages_with_history(self):
        """Prepare messages with chat history context for the graph."""
        # If we have chat history, include it in the context
        if self.chat_history:
            # Convert chat history to LangChain message format
            messages = []
            for msg in self.chat_history[-10:]:  # Keep last 10 messages for context
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

            # Add the current user message
            messages.append(HumanMessage(content=self.user_message))
            return messages
        else:
            # No history, just return the current message
            return ("user", self.user_message)

    def display_chat_history(self):
        """Display the full chat history."""
        if self.chat_history:
            st.subheader("Chat History")
            for i, msg in enumerate(self.chat_history):
                with st.chat_message(msg["role"]):
                    st.write(f"**Message {i+1}:** {msg['content']}")
        else:
            st.info("No chat history available.")

    def get_chat_context_summary(self, max_messages=5):
        """Get a summary of recent chat context."""
        if not self.chat_history:
            return "No previous conversation context."

        recent_messages = self.chat_history[-max_messages:]
        context_summary = "Recent conversation context:\n"

        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_summary += f"{role}: {msg['content'][:100]}...\n"

        return context_summary