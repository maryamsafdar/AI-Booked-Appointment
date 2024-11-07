from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, MessagesState
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from tools import book_appointment, get_next_available_appointment, cancel_appointment
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
# Initialize language model with the specific model
# Initialize the Language Model
llm = ChatGroq(model="llama-3.1-8b-instant")
CONVERSATION = []

def receive_message(message):
    """Appends user message to the conversation and processes it."""
    CONVERSATION.append(HumanMessage(content=message, type="human"))
    state = {"messages": CONVERSATION}
    print(state)
    new_state = assistant_app.invoke(state)
    CONVERSATION.extend(new_state["messages"][len(CONVERSATION):])

def should_continue(state: MessagesState):
    """Condition to decide if the assistant should continue or end."""
    last_message = state["messages"][-1]
    return "continue" if last_message.tool_calls else "end"

def assistant_model(state: MessagesState):
    """Invokes the assistant model based on the current state."""
    state["current_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    response = assistant_model.invoke(state)
    return {"messages": [response]}

tools = [book_appointment, get_next_available_appointment, cancel_appointment]
tool_node = ToolNode(tools)

assistant_prompt = """You are a personal assistant. Help the user to book or cancel appointments. Check availability before booking.
Current time: {current_time}"""

assistant_template = ChatPromptTemplate.from_messages([
    ("system", assistant_prompt),
    ("placeholder", "{messages}")
])

assistant_model = assistant_template | llm.bind_tools(tools)

workflow = StateGraph(MessagesState)
workflow.add_node("agent", assistant_model)
workflow.add_node("action", tool_node)

workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
workflow.add_edge("action", "agent")
workflow.set_entry_point("agent")

assistant_app = workflow.compile()
