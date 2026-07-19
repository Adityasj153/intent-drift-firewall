from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.calculator import calculator

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

question = input("Ask me anything: ")

if any(op in question for op in ["+", "-", "*", "/"]):
    print("Using calculator....")
    answer = calculator(question)
    print(answer)

else:
    response = llm.invoke(question)
    print(response.content)

