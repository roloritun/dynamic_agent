from langchain.agents import AgentExecutor, create_openai_tools_agent, create_structured_chat_agent
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from api_tool import create_api_tools
from db_tool import create_db_tools
#from builtin_tool import create_builtin_tools
from database import session
from prompt import get_prompt_for_structured_agent
from utils import Llm


llm = Llm.get_llm()
api_tools = create_api_tools(session)
db_tools = create_db_tools(session)
#builtin_tools = create_builtin_tools(session)Y
    
all_tools = api_tools + db_tools  #+ builtin_tools
@staticmethod
def create_langchain_agent():
   
    prompt = get_prompt_for_structured_agent()
    agent = create_structured_chat_agent(
        llm=llm,
        tools=all_tools,
        prompt=prompt
    )

    return agent

def create_db_langchain_agent():

    # Use StructuredChatAgent if needed
    agent = create_sql_agent(llm=llm, tools=db_tools)

    return agent


""" 
def create_builtin_langchain_agent():


    agent = create_structured_chat_agent(
        llm=llm,
        tools=builtin_tools,
        verbose=True
    )

    return agent """

def create_api_langchain_agent():


    agent = create_openai_tools_agent(
        llm=llm,
        tools=api_tools,
        verbose=True
    )

    return agent

if __name__ == "__main__":

    agent = create_langchain_agent()

    # Sample query input
    #user_input = "I am new client and my name is James Burden and my email is james@example.com "
    user_input = "Tell me a recipe for italian pasta"
    tool = agent.as_tool()
    #user_input = "What is th e current weather in London"
    agent_executor = AgentExecutor( 
            agent=agent,
            tools=all_tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,            
        )
    #result = agent_executor.invoke({"input": question})

    # Invoke the agent and print the output
    response = agent_executor.invoke({"input": user_input})

    print("Agent Response:", response)