from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import AgentRunner
import os
from dotenv import load_dotenv

load_dotenv()

llm_url = os.getenv("LLM_URL")
model = os.getenv("LLM")


# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result"""
    return (a * b)

def divide(a: int,b: int) -> float:
    """Divides two numbers and returns the result"""
    return (a//b)


multiply_tool = FunctionTool.from_defaults(fn=multiply)
divide_tool = FunctionTool.from_defaults(fn=divide)

# initialize llm
llm = Ollama(model=model,request_timeout=120, base_url=llm_url)

# initialize ReAct agent
agent = AgentRunner.from_llm([multiply_tool,divide_tool], llm=llm, verbose=True)
agent.chat("what is 25 / 25")
