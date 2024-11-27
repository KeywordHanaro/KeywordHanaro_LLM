import os
from openai import OpenAI
from dotenv import load_dotenv

# API KEY 호출
# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("GPT_API_KEY")
#
# client = OpenAI()

from llm.MetaData import getTopMeta

def getAnswer(user_query):
    return getTopMeta(user_query)