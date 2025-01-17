from config import *

from aiogram import F, Router, html

from aiogram import Bot, Dispatcher, types
import openai
from openai import OpenAI
from typing import Any
from dataclasses import dataclass, field
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA, LLMChain
from langchain_openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from .questions import documents

api_key = load_config().openai_token.token

df = pd.read_csv("document_questions.csv")
loader = DataFrameLoader(df, page_content_column='question')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
db = FAISS.from_documents(texts, embeddings, distance_strategy="COSINE")


prompt_template = """Выведи и сократи до 100 слов следующий текст: "{answer}"
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=['answer']
)

llm = OpenAI(temperature=0, openai_api_key=api_key, max_tokens=500)

chain = PROMPT | llm | StrOutputParser()

default_router = Router()

@default_router.message()
async def reply_to_any_message(message: types.Message):
    try:
        relevants = db.similarity_search_with_score(message.text)
        if relevants:
            all_doc = [f"{answer.page_content}" + "\n" + answer.metadata["answer"] + "\n\n" for answer, score in relevants if 1-score>0.45]
            if len(all_doc) >= 2:
                all_doc = all_doc[:2]
            elif not all_doc:
                all_doc.append("Можете, пожалуйства, переформулировать или уточнить вопрос?")

            ans = "".join(all_doc)
            response = await chain.ainvoke(ans)
            await message.answer(response)
        else:
            await message.answer("Извините, я не нашел информации по вашему вопросу.")
    except Exception as e:
        print(e)
        await message.answer("Произошла ошибка при обработке вашего запроса.")