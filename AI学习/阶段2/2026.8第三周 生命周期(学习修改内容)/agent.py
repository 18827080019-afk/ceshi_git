
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
        self.update_state("status", "running")
        self.update_state("task",user_input)
        self.trace.add_step("user_input", user_input)

    def run(self,user_input):
            self._start_run(user_input)
            step_count = 0
            while step_count < self.max_steps:#return结果时,循环结束
                response=self.step(user_input)
                protocol_answer=self.protocol(response)
                if protocol_answer is not None:
                    self.state.append_context("protocol_errors", protocol_answer)
                    self.trace.add_step("protocol_error", protocol_answer)
                    step_count += 1
                    continue

                else:
                    result=self.handle_action(response)
                   
    
                if result is not None:
                    self.update_state("status","success")
                    self.update_memory("user",user_input)
                    self.update_memory("assistant",result)
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

    
    #同executor,检验层********************************
    def protocol(self,response):

        if not isinstance(response,dict):
            
            return{
                "type":"protocol_error",
                "code":"Incorrect data type",
                "field":"response",
                "message":"Incorrect data type:response",
                "recoverable":True,
                "response":response
            }
            
        else:
            
            if "action" not in response:
                return{
                                "type":"protocol_error",
                                "code":"missing field",
                                "field":"action",
                                "message":"missing field: action",
                                "recoverable":True,
                                "response":response
                            }
            else:
                action=response.get("action")
                if action=="tool":
                   
                    if "args" not in response:
                        return{
                                "type":"protocol_error",
                                "code":"missing field",
                                "field":"args",
                                "message":"missing field: args",
                                "recoverable":True,
                                "response":response
                            }
                    elif not isinstance(response["args"],dict):
                        return{
                                "type":"protocol_error",
                                "code":"Incorrect data type",
                                "field":"args",
                                "message":"Incorrect data type:args",
                                "recoverable":True,
                                "response":response
                            }                
                
                    if "tool" not in response:
                        return{
                                "type":"protocol_error",
                                "code":"missing field",
                                "field":"tool",
                                "message":"missing field: tool",
                                "recoverable":True,
                                "response":response
                            }
                    elif not isinstance(response["tool"],str):
                        return{
                                "type":"protocol_error",
                                "code":"Incorrect data type",
                                "field":"tool",
                                "message":"Incorrect data type:tool",
                                "recoverable":True,
                                "response":response
                            }

                elif action=="final":
                    if "answer" not in response:
                        return{
                                "type":"protocol_error",
                                "code":"missing field",
                                "field":"answer",
                                "message":"missing field: answer",
                                "recoverable":True,
                                "response":response
                            }
                    
                    elif not isinstance(response["answer"],str):
                        return{
                                "type":"protocol_error",
                                "code":"Incorrect data type",
                                "field":"answer",
                                "message":"Incorrect data type:answer",
                                "recoverable":True,
                                "response":response
                            }
                        
                else:
                    return{
                                "type":"protocol_error",
                                "code":"Invaild enum value",
                                "field":"action",
                                "message":"Invaild enum value:action=final/tool",
                                "recoverable":True,
                                "response":response
                            }
                    
            
                    
    def step(self,user_input):
            context = self.context_builder.build(user_input,self.state,self.memory.get_memory(),self.llm_tools_context)
            messages = self.prompt_builder.build(context)
    
            response = self.llm.chat(messages)
            self.trace.add_step("llm_response",response)
            return response

    def handle_action(self,response):
            action=response.get("action")
    
            if action=="final":
    
                answer=response["answer"]
                
                self.trace.add_step("final_answer", answer)
                return answer
    
            if action=="tool":
                result=self.execute_tool(response)
                self.state.append_context("tool_result", result)      
                return None
    
            
    