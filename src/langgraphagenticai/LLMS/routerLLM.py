import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import Literal

llm=ChatGroq(model="qwen-qwq-32b")

class Route(BaseModel):
    """
    This is the model for the router.
    It is used to route the user to the next step in the routing process.
    The step is the next step in the routing process.
    The step is one of the following:
    - email_node
    - calender_node
    - store_node
    - chat_node
    - agenticAI
    """
    step:Literal["email_node","calender_node","store_node","chat_node","agenticAI"]=Field(description="The next step in the routing process")



class Router:
    def __init__(self,user_controls_input, message):
        self.user_controls_input=user_controls_input
        self.message=message
          
    def router_change_step(self,user_controls_input):
        groq_api_key=user_controls_input["GROQ_API_KEY"]
        selected_router_model=self.user_controls_input["selected_router_model"]
        router_llm=ChatGroq(api_key=groq_api_key,model=selected_router_model)
        router_structure=router_llm.with_structured_output(Route)
        decision=router_structure.invoke(
            [
                SystemMessage(
                    content="""
                        Route the input to calender, email, storing data or restaurant chat, parking chat, agentic chat based on the users request.
                        if the user request is about restaurant or parking or combination of restaurant and parking, then route to chat.
                        if the user request is about calender, then route to calender.
                        if the user request is about email, then route to email.
                        if the user request is about storing data, then route to store.
                        if the user request is about combination of restaurant or parking, calender, email, store, chat, then route to agentic chat or not in the list then route to chat.
                    """
                ),
                HumanMessage(content=self.message)
            ]
        )
        return decision.step

if __name__ == "__main__":
    user_controls_input={
        "GROQ_API_KEY":os.getenv("GROQ_API_KEY"),
        "selected_router_model":"qwen-qwq-32b"
        }
    message="what is the best parking spot near to the restaurant sasao and save the details in the calender"
    router=Router(user_controls_input, message)
    print(router.router_change_step(user_controls_input))

