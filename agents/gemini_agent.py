from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

def ask_gemini(question):
    response = llm.invoke(question)
    return response.content
