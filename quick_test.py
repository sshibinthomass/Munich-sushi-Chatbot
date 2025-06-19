from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import asyncio #asyncio is a library for asynchronous programming in Python.
load_dotenv()

async def main():
    #MultiServerMCPClient is a client that can connect to multiple MCP servers.
    client=MultiServerMCPClient( 
        {
            "sushi": {
                "url": "http://127.0.0.1:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            }
        }
    )

    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    agent=create_react_agent(
        model,tools
    )

    restaurant_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What are available sushi restaurants?"}]}
    )

    print("Sushi response:", restaurant_response['messages'][-1])

if __name__ == "__main__":
    asyncio.run(main())
