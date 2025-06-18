# This class is used to load the config file and get the options for the UI
from configparser import ConfigParser
import requests
import os
import streamlit as st
import ollama

@st.cache_data(show_spinner="Loading Groq models...")
def fetch_groq_model_options():
    #GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    #response = requests.get(
    #    "https://api.groq.com/openai/v1/models",
    #    headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
    #)
#
    #if response.status_code == 200:
    #    data = response.json()["data"]
    #    text_models = [
    #        m["id"]
    #        for m in data
    #        if any(
    #            prefix in m["id"].lower()
    #            for prefix in ["llama", "mixtral", "gemma"]
    #        )
    #    ]
    #    return text_models 
    #else:
    #    print("Error:", response.status_code, response.text)
    #    return []
    return ["Gemma2-9b-It"]

@st.cache_data(show_spinner="Loading Ollama models...")
def fetch_ollama_model_options():
    models = ollama.list()
    model_names = [model['model'] for model in models['models']]
    return model_names

@st.cache_data(show_spinner="Loading OpenAI models...")
def fetch_openai_model_options():
    return ["gpt-4.1-mini"]

class Config:
    def __init__(self,config_file="./src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)
        self.config_file=config_file
    
    #Use split to split the options into a list
    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_usecase_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")

    def get_groq_model_options(self):
        return fetch_groq_model_options()

    def get_ollama_model_options(self):
        return fetch_ollama_model_options()

    def get_openai_model_options(self):
        return fetch_openai_model_options()

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
