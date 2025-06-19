import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

#Import the config file
#from file location and name import class
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config() #Config class is imported from the config file(uiconfigfile.py)
        self.user_controls={} #This is a dictionary to store the user controls

    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide") #This is the title of the streamlit app
        st.header("🤖 " + self.config.get_page_title()) #This is the header of the streamlit app from the config file

        with st.sidebar: #This is the sidebar of the streamlit app
            # Get options from config
            llm_options = self.config.get_llm_options() #This is a list of LLM options from the config file
            usecase_options = self.config.get_usecase_options() #This is a list of Usecase options from the config file

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq': #This is the Groq model selection
                # Model selection
                model_options = self.config.get_groq_model_options() #This is a list of Groq model options from the config file
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options) #This is the Groq model selection
                self.user_controls["GROQ_API_KEY"] =os.getenv("GROQ_API_KEY")

            if self.user_controls["selected_llm"] == 'OpenAI': #This is the OpenAI model selection
                # Model selection
                model_options = self.config.get_openai_model_options() #This is a list of OpenAI model options from the config file
                self.user_controls["selected_openai_model"] = st.selectbox("Select Model", model_options) #This is the OpenAI model selection
                self.user_controls["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

            ## USecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options) #This is the Usecase selection from the config file

        return self.user_controls