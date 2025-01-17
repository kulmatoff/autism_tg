from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from config import *

def get_completion(
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=300,
    message=None,
    prompt=None
):
    chat = ChatOpenAI(
        api_key=load_config().openai_token.token,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    messages = []
    
    if prompt:
        messages.append(SystemMessage(content=prompt))
    
    if message:
        messages.append(HumanMessage(content=message))
    
    response = chat(messages)
    return response.content
