from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from database import DatabaseConnection
from dotenv import find_dotenv, load_dotenv
from utils import Llm



def create_db_tools(session):
    _ = load_dotenv(find_dotenv())  # read local .env file

    llm = Llm.get_llm()
    
    db_connections = session.query(DatabaseConnection).all()
    tools = []

    for db in db_connections:
        # Initialize the SQLDatabase using the connection string
        sql_database = SQLDatabase.from_uri(db.connection_string)
        toolkit = SQLDatabaseToolkit(llm=llm, db=sql_database)

        # Add all SQL tools (e.g., SQL query, table information) to the tools list

        stools = toolkit.get_tools()
        for t in stools:
            t.name = db.name +"_"+t.name
            t.description =db.description +". " +t.description
        tools.extend(stools)
    
    return tools
