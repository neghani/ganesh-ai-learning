import os
from dotenv import load_dotenv;
from langchain.chat_models import init_chat_model;
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts.prompt import  PromptTemplate;

load_dotenv()

template = """a"""
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

chain = PromptTemplate(list[str],template);

for token in model.stream(messages):
    print(token.content, end="|")
