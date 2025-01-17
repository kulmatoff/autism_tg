from config import *

# import openai
# from openai import OpenAI
# from typing import Any
# from dataclasses import dataclass, field
# import pandas as pd
# from langchain.document_loaders import DataFrameLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA, LLMChain
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain import HuggingFaceHub

api_key = load_config().openai_token.token

# df = pd.DataFrame(documents)
# loader = DataFrameLoader(df, page_content_column='question')
# documents = loader.load()

# # Создание векторного хранилища
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)
# embeddings = OpenAIEmbeddings(openai_api_key=api_key)
# db = FAISS.from_documents(texts, embeddings)

# # Создание цепочки вопрос-ответ
# qa_chain = RetrievalQA.from_chain_type(
#     llm=OpenAI(temperature=0, openai_api_key=api_key),
#     chain_type='stuff',
#     retriever=db.as_retriever()
# )

# # Создание шаблона ответа
# prompt_template = """Используй контекст для ответа на вопрос, пользуясь следующими правилами:
# Не изменяй текст, который находится в кавычках.
# {answer}
# """

# PROMPT = PromptTemplate(
#     template=prompt_template,
#     input_variables=['answer']
# )

# # Создание цепочки обработки
# chain = LLMChain(
#     llm=OpenAI(temperature=0, openai_api_key=api_key, max_tokens=500),
#     prompt=PROMPT
# )