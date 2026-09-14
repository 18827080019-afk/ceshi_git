
from trace import Trace
from state import State
class Agent:

    def __init__(self,memory,llm,context_builder,prompt_builder,executor,llm_tools_context):
        self.memory = memory
        self.llm = llm
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.executor = executor
        self.llm_tools_context = llm_tools_context

        self.max_steps=10
        self.state = None
        self.trace = None

    def _start_run(self,user_input):
        self.trace = Trace()
        self.state = State()
        self.executor.trace = self.trace
        self.update_memory("user",user_input)
        self.update_state("task",user_input)
        self.update_state("status", "running")
        self.trace.add_step("user_input", user_input)

    def run(self,user_input):
        self._start_run(user_input)
        step_count = 0
        while step_count < self.max_steps:#return结果时,循环结束
            response=self.step(user_input)
            result=self.handle_action(response)

            if result is not None:
                self.update_state("status","success")
                return result
            step_count += 1
        self.update_state("status","max_steps")
        return "超过最大循环次数"

    def update_memory(self,role,content):
        self.memory.add_memory(role,content)

    def update_state(self,key,value):
        self.state.update(key,value)

    def execute_tool(self,response):
        tool_name=response["tool"]
        args=response["args"]
        result=self.executor.execute(tool_name,**args)
        return result

    def handle_action(self,response):
        action=response.get("action")

        if action=="final":
            answer=response["answer"]
            self.update_memory("assistant",answer)
            self.trace.add_step("final_answer", answer)
            return answer

        if action=="tool":
            result=self.execute_tool(response)
            self.update_memory("tool", result)
            self.state.update_context("result", result)

                    # if result.get("status")=="error":
                    #     self.state.update_context("tool_status","error")
                    # else:
                    #     self.state.update_context("tool_status","success")
                                                  
            return None
        



    def step(self,user_input):
            context = self.context_builder.build(user_input,self.state,self.memory.get_memory(),self.llm_tools_context)
            messages = self.prompt_builder.build(context)
    
            response = self.llm.chat(messages)
            self.trace.add_step("llm_response",response)
            return response