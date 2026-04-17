from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def call_model(state):
    prompt = SystemMessage(content="You are a Mobile Architect. Use tools to read the failing test file and write a fix. Only use 'write_file' if you are sure.")
    # Bind tools to the LLM
    agent = llm.bind_tools([*state['tools']])
    response = agent.invoke([prompt] + state['messages'])
    return {"messages": [response]}

def should_continue(state):
    last_msg = state['messages'][-1]
    return "action" if last_msg.tool_calls else "end"
