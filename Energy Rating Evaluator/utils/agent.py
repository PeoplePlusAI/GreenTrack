from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.env import GROQ_API_KEY, GROQ_CHAT_MODEL, OPENAI_API_KEY, OPENAI_CHAT_MODEL
from utils.io import read_file

if GROQ_API_KEY:
    chat_agent = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=GROQ_CHAT_MODEL)
    prompts_path = "prompts/groq"
elif OPENAI_API_KEY:
    chat_agent = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=OPENAI_CHAT_MODEL)
    prompts_path = "prompts/openai"
else:
    raise Exception("No valid API key found.")

def call_agent(replacer, prompt_file):
    try:
        extraction_prompt = PromptTemplate(
            template=read_file(f"{prompts_path}/{prompt_file}"),
            input_variables=["placeholder"],
        )
        extract_from = extraction_prompt | chat_agent | StrOutputParser()
        prompt_input = {"placeholder": replacer}
        response = extract_from.invoke(prompt_input)
        return response.strip()
    except:
        raise Exception("API Limit Reached. Please try again later.")
