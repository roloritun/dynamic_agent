import re
from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


import os


class Llm:
    def __init__(self):
        pass

    @staticmethod
    def get_llm():

        _ = load_dotenv(find_dotenv())  # read local .env file

        # openai.api_key = os.environ["OPENAI_API_KEY"]
        # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        llm = AzureChatOpenAI(
          azure_deployment="16_deploy",
        )
        # llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        return llm
    
    
def remove_special_characters(string):
    return re.sub(r'[^a-zA-Z0-9]', '', string)


