import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import openai
from langchain import hub
from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# API KEY 호출
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("GPT_API_KEY")
#
# client = OpenAI()

from llm.MetaData import getTopMeta

def format_docs(docs):
    # 검색한 문서 결과를 하나의 문단으로 합치기
    return "\n\n".join(doc.page_content for doc in docs)

def getAnswer(user_query):
    metaData = getTopMeta(user_query)
    if metaData["similarity_score"] <0.05:
        return "유사도 에러"
    filePath = f"./doc/{metaData['contents_type']}/{metaData['category']}/{metaData['fileName']}.pdf"
    loader = PyPDFLoader(filePath)
    docs = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    openai_embeddings = OpenAIEmbeddings(api_key=openai.api_key)
    vectorstore = FAISS.from_documents(documents=splits, embedding=openai_embeddings)
    retriever = vectorstore.as_retriever()

    prompt = hub.pull("rlm/rag-prompt")

    class StreamCallback(BaseCallbackHandler):
        def on_llm_new_token(self, token: str, **kwargs):
            print(token, end="", flush=True)

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[StreamCallback()],
    )

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    answer = rag_chain.invoke(user_query)
    return answer