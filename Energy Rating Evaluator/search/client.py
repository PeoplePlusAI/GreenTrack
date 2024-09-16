from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from utils.env import GROQ_API_KEY, GROQ_CHAT_MODEL
from utils.io import read_file

chat = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=GROQ_CHAT_MODEL)

extraction_prompt = PromptTemplate(
    template=read_file("static/star_rating_prompt.txt"),
    input_variables=["features"],
)
extract_from = extraction_prompt | chat | StrOutputParser()

def extract_rating(features):
    try:
        prompt_input = {"features": '\n'.join(features)}
        response = extract_from.invoke(prompt_input)
        return response.strip()
    except:
        raise Exception("Groq API Limit Reached. Please try again later.")
