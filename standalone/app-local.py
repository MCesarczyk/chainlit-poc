from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import chainlit as cl
from typing import Optional

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

ollama = OllamaLLM(
    model="hf.co/SunJack/Qwen2-0.5b-finetuning:Q4_K_M",
    base_url="http://ollama:11434"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful bot, you always reply in Bulgarian"),
    ("user", "{question}")
])

chain = prompt | ollama

@cl.on_chat_start
async def start():
    cl.user_session.set("chain", chain)

@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    msg = cl.Message(content="")

    async for chunk in chain.astream(
        {"question": message.content},
    ):
        await msg.stream_token(chunk)

    await msg.send()
