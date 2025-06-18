import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,graph,user_message,selected_llm=None):
        self.graph = graph
        self.user_message = user_message
        self.selected_llm = selected_llm

    def display_result_on_ui(self):
        graph = self.graph
        user_message = self.user_message
        selected_llm = self.selected_llm
        for event in graph.stream({'messages':("user",user_message)}):
            for value in event.values():
                with st.chat_message("user"):
                    st.write(user_message)
                with st.chat_message("assistant"):
                    if selected_llm == "Groq" or selected_llm == "OpenAI":
                        st.write(value["messages"].content)
                    else:
                        st.write(value["messages"])

    def get_assistant_response(self):
        graph = self.graph
        user_message = self.user_message
        selected_llm = self.selected_llm
        for event in graph.stream({'messages': ("user", user_message)}):
            for value in event.values():
                if selected_llm == "Groq" or selected_llm == "OpenAI":
                    return value["messages"].content
                else:
                    return value["messages"]