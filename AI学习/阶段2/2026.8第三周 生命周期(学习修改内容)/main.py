import os
from pathlib import Path
from dotenv import load_dotenv

from agent import Agent
from ai import LLM
from executor import Executor
from memory import Memory
from tool_functions import (add_tool, multiply_tool)
from models.register import Registry
from adapter import build_tool_context
from context import ContextBuilder
from prompt import PromptBuilder
from trace import Trace
from state import State
def main():
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请在项目根目录 .env 中设置 DEEPSEEK_API_KEY")

    registry=Registry()
    registry.register(add_tool)
    registry.register(multiply_tool)

    executor=Executor(registry, None)
    
    contextBuilder=ContextBuilder()
    llm_tools_context=build_tool_context(registry)#加载完成工具信息
    promptBuilder=PromptBuilder()

    memory = Memory()
    llm = LLM(model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"), api_key=api_key, base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    agent=Agent(memory,llm,contextBuilder,promptBuilder,executor,llm_tools_context)
    while True:
        user_input = input("\nUser: ")
        if user_input == "exit":
            break
        result = agent.run(user_input)
        print("State:",agent.state.get())
        print("Trace:",agent.trace.get_trace())
        print("Memory:",agent.memory.get_memory())

        print(f"Assistant: {result},记录:{agent.trace.get_trace()}")
        
if __name__ == "__main__":
    main()