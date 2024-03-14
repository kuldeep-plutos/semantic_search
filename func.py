from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import AgentRunner


# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)

# initialize llm
llm = Ollama(model="gemma:2b",request_timeout=120)

# initialize ReAct agent
agent = AgentRunner.from_llm([multiply_tool], llm=llm, verbose=True)
res = agent.chat("what is 5521 multiplied by 20")
print(res)