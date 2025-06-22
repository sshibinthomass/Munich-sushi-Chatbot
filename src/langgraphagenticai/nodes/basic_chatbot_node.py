from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
import sys
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import asyncio #asyncio is a library for asynchronous programming in Python.
from pathlib import Path
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))
from src.langgraphagenticai.state.state import State
load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

class StorageDecision(BaseModel):
    should_store: bool = Field(description="Whether to store the information - true or false")
    message_to_store: str = Field(description="The clean, concise message to store (empty if not storing)")
    reason: str = Field(description="Reason for the storage decision")
    is_duplicate: bool = Field(description="Whether this information is similar to existing stored information")


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

    def retrieve_node(self,state:State)->dict:
        """
        Processes the input state and retrieves information from the long term memory.
        """
        messages = state["messages"]
        if not messages:
            return {"messages": "No messages to process"}
        
        # Get the last message content
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            user_input = last_message.content
        elif isinstance(last_message, dict) and 'content' in last_message:
            user_input = last_message['content']
        else:
            user_input = str(last_message)
        embedding=OpenAIEmbeddings()
        db = Chroma(persist_directory="./chroma_openai", embedding_function=embedding)
        docs=db.similarity_search(user_input)
        retrieved_info = "\n".join([f"Document: {doc.page_content}" for doc in docs])
        return {"retrieved_info": retrieved_info}

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
            print(state['messages'])
            retrieved_info=self.retrieve_node(state)
            rag_system_message = SystemMessage(
                content=f"Relevant information retrieved for this query based on personal information:\n\n{retrieved_info}"
            )
            base_system_msg = state["messages"][0]
            conversation = state["messages"][1:]
            messages = [base_system_msg, rag_system_message] + conversation
            response = await agent.ainvoke(
                {"messages": messages}
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
    

    def store_node(self,state:State)->dict:
        """
        Processes the input state and decides whether to store information in a single LLM call.
        """
        # Extract the last user message content from the messages list
        messages = state["messages"]
        if not messages:
            return {"messages": "No messages to process"}
        
        # Get the last message content
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            user_input = last_message.content
        elif isinstance(last_message, dict) and 'content' in last_message:
            user_input = last_message['content']
        else:
            user_input = str(last_message)
        embedding=OpenAIEmbeddings()
        # db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)
        # docs=db.similarity_search(user_input)
        # retrieved_info = "\n".join([f"Document: {doc.page_content}" for doc in docs])
        
        retrieved_info=self.retrieve_node(state)
        print(retrieved_info['retrieved_info'])
        # Single LLM call to make all decisions
        llm_with_structured = self.llm.with_structured_output(StorageDecision)
        response = llm_with_structured.invoke([
            SystemMessage(content="""
                You are a helpful assistant that decides whether to store user information.
                
                Rules:
                1. Store information if it contains personal details (name, age, location, contact info) or preferences (likes/dislikes)
                2. Do NOT store if the information is too similar to existing stored information
                3. Do NOT store general questions, weather queries, or non-personal information
                4. Create a clean, concise version for storage that's easy to retrieve
                
                Return:
                - should_store: true only if information should be stored AND is not duplicate
                - message_to_store: clean version of the information (empty if not storing)
                - reason: explanation of your decision
                - is_duplicate: true if information is too similar to existing data
                """),
            HumanMessage(content=f"""
                User input: {user_input}
                Retrieved information: {retrieved_info}
                
                Should I store this information?
                """)
        ])
        
        # Store if decision is to store
        if response.should_store and response.message_to_store:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
            splits = text_splitter.split_text(response.message_to_store)
            vectordb=Chroma.from_texts(texts=splits,embedding=embedding,persist_directory="./chroma_openai")
        
        result={
            "stored": response.should_store,
            "reason": response.reason,
            "is_duplicate": response.is_duplicate,
            "message_to_store": response.message_to_store,
        }
        #print(result)
        return result

if __name__ == "__main__":
    # Create LLM instance
    llm = ChatGroq(model="qwen-qwq-32b")
    
    # Create RestaurantRecommendationNode instance with the LLM
    node = RestaurantRecommendationNode(llm)
    
    # Test the store_node method
    result = node.store_node(state={"messages": "What is the weather in Munich?"})
    print("Store Node Result:", result)
    
    # Test with personal information 
    result2 = node.store_node(state={"messages": "Mr Luke is a good person"})
    print("Store Node Result (Personal Info):", result2)
