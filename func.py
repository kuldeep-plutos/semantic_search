from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent


# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result"""
    return (a * b)

def divide(a: int,b: int) -> float:
    """Divides two numbers and returns the result"""
    return (a/b)


multiply_tool = FunctionTool.from_defaults(fn=multiply)
divide_tool = FunctionTool.from_defaults(fn=divide)

# initialize llm
llm = Ollama(model="phi",request_timeout=120)

# initialize ReAct agent
agent = ReActAgent.from_tools([multiply_tool,divide_tool], llm=llm, verbose=True)
agent.chat("divide 5555 by 111")