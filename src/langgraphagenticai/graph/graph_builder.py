from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode,RestaurantRecommendationNode
from src.langgraphagenticai.nodes.assistant_chatbot_node import AgenticAIChatbotNode
from src.langgraphagenticai.LLMS.routerLLM import Router
from src.langgraphagenticai.nodes.assistant_chatbot_node import AgenticAIChatbotNode
import asyncio
from dotenv import load_dotenv
load_dotenv()

class GraphBuilder:
    def __init__(self,model,user_controls_input,message):
        self.llm=model
        self.user_controls_input=user_controls_input
        self.message=message
        self.current_llm=user_controls_input["selected_llm"]
        self.graph_builder=StateGraph(State)  #StateGraph is a class in LangGraph that is used to build the graph

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node=BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def chatbot_restaurant_recommendation(self):
        """
        Builds a chatbot graph for sushi recommendations.
        """
        self.restaurant_recommendation_node=RestaurantRecommendationNode(self.llm)

        self.graph_builder.add_node("chatbot",self.restaurant_recommendation_node.process_sync)
        self.graph_builder.add_node("store_node",self.restaurant_recommendation_node.store_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot","store_node")
        self.graph_builder.add_edge("chatbot",END)

    def assistant_chatbot_build_graph(self):
        """
        Builds a assistant chatbot graph using LangGraph.
        """
        self.restaurant_recommendation_node=RestaurantRecommendationNode(self.llm)
        self.agentic_ai_chatbot_node=AgenticAIChatbotNode(self.llm)
        self.router_llm = Router(user_controls_input=self.user_controls_input, message=self.message)

        self.graph_builder.add_node("agent_node",self.agentic_ai_chatbot_node.agent_node)
        self.graph_builder.add_node("chat_node",self.restaurant_recommendation_node.process)
        self.graph_builder.add_node("store_node",self.agentic_ai_chatbot_node.store_node)
        self.graph_builder.add_node("retrieve_node",self.agentic_ai_chatbot_node.retrieve_node)
        self.graph_builder.add_node("email_node",self.agentic_ai_chatbot_node.email_node)
        self.graph_builder.add_node("calender_node",self.agentic_ai_chatbot_node.calender_node)

        # Define routing function (this is the key fix)
        def route_to_node(state):
            """Route to appropriate node based on router decision"""
            try:
                # Get router decision
                router_result = self.router_llm.router_change_step(self.user_controls_input)
                
                # Map router output to node names
                if router_result == "email_node":
                    return "email_node"
                elif router_result == "calender_node":
                    return "calender_node"
                elif router_result == "store_node":
                    return "store_node"
                elif router_result == "chat_node":
                    return "chat_node"
                elif router_result == "agenticAI":
                    return "agent_node"  # Loop back to agent for complex requests
                else:
                    return "chat_node"  # Default fallback
            except Exception as e:
                print(f"Router error: {e}")
                return "chat_node"  # Default fallback


        self.graph_builder.add_edge(START,"agent_node")

        self.graph_builder.add_conditional_edges(
            "agent_node",
            route_to_node,
            {
                "chat_node": "chat_node",
                "store": "store_node",
                "retrieve": "retrieve_node",
                "email": "email_node",
                "calender": "calender_node"
            }
        )

        self.graph_builder.add_edge("chat_node","agent_node")
        self.graph_builder.add_edge("store_node","agent_node")
        self.graph_builder.add_edge("retrieve_node","agent_node")
        self.graph_builder.add_edge("email_node","agent_node")
        self.graph_builder.add_edge("calender_node","agent_node")
        self.graph_builder.add_edge("agent_node",END)
        self.graph_builder.add_edge("chat_node",END)


    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case.
        """

        if usecase == "Sushi":
           self.chatbot_restaurant_recommendation()
        elif usecase == "Agentic AI":
           self.assistant_chatbot_build_graph()
        else:
           self.basic_chatbot_build_graph()

        return self.graph_builder.compile()
