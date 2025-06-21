from src.langgraphagenticai.state.state import State
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
import os
from dotenv import load_dotenv
import asyncio #asyncio is a library for asynchronous programming in Python.
load_dotenv()

class BasicChatbotNode:
    """
    Basic Chatbot login implementation
    """
    def __init__(self,model):
        self.llm=model

    def process(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        response = self.llm.invoke(state['messages'])
    
    #Error handling for the response 
        # If response is an AIMessage, extract .content
        if hasattr(response, "content"):
            return {"messages": response.content}
        # If response is a dict with 'content', extract it
        if isinstance(response, dict) and 'content' in response:
            return {"messages": response['content']}
        # If response is a string, return as is
        return {"messages": response}

class RestaurantRecommendationNode:
    """
    Restaurant Recommendation Node  
    """
    def __init__(self,model):
        self.llm=model

    async def process(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        try:
            #MultiServerMCPClient is a client that can connect to multiple MCP servers.
            client=MultiServerMCPClient( 
                {
                    "restaurant":{
                        "url": "http://127.0.0.1:8002/mcp", 
                        "transport": "streamable_http",
                    },
                    "Parking":{
                        "url": "http://127.0.0.1:8003/mcp", 
                        "transport": "streamable_http",
                    }
                }
            )
            os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
            tools=await client.get_tools()
            model=self.llm
            agent=create_react_agent(
                model, tools
            )
            response = await agent.ainvoke(
                {"messages": state['messages']}
            )
        except Exception as e:
            print(e)
            return {"messages": "Error: " + str(e)}
        return {"messages": AIMessage(content=response['messages'][-1].content)}
    
    #When called async directly from graph builter it gave error so added a sync function which calls the asyncio function
    def process_sync(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return asyncio.run(self.process(state))
