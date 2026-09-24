from trace import Trace
from state import State
from Protocol import ProtocolValidator
from runtime_result import run_success,run_failed


class Agent:

    def __init__(
        self,
        memory,
        llm,
        context_builder,
        prompt_builder,
        executor,
        llm_tools_context
    ):
        self.memory = memory
        self.llm = llm
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.executor = executor
        self.llm_tools_context = llm_tools_context

        self.protocol_validator = ProtocolValidator()

        self.max_steps = 10

        self.state = None
        self.trace = None


    def _start_run(self,user_input):

        self.trace = Trace()
        self.state = State()

        self.executor.trace = self.trace

        self.update_state(
            "task",
            user_input
        )

        self.update_state(
            "status",
            "running"
        )

        self.trace.add_step(
            "user_input",
            user_input
        )


    def run(self,user_input):

        self._start_run(
            user_input
        )

        step_count = 0

        while step_count < self.max_steps:

            # 一次while = 一次LLM决策
            response = self.step(
                user_input
            )

            step_count += 1


            # 1. Protocol Boundary
            protocol_error = (
                self.protocol_validator.validate(
                    response
                )
            )

            if protocol_error is not None:

                self.state.append_context(
                    "protocol_errors",
                    protocol_error
                )

                self.trace.add_step(
                    "protocol_error",
                    protocol_error
                )

                # 当前协议错误可恢复
                if protocol_error["recoverable"]:
                    continue

                # 不可恢复协议错误
                self.update_state(
                    "status",
                    "failed"
                )

                return run_failed(
                    protocol_error
                )


            # 2. 合法Action
            result = self.handle_action(
                response
            )


            # Tool Action
            # result=None
            # 下一轮重新让LLM决策
            if result is None:
                continue


            # 3. Final
            self.update_state(
                "status",
                "success"
            )

            self.update_memory(
                "user",
                user_input
            )

            self.update_memory(
                "assistant",
                result
            )

            return run_success(
                result
            )


        # 4. Runtime最终失败
        runtime_error = {
            "type":"runtime_error",
            "code":"max_steps",
            "message":"agent exceeded max steps"
        }

        self.state.update_context(
            "runtime_error",
            runtime_error
        )

        self.trace.add_step(
            "runtime_error",
            runtime_error
        )

        self.update_state(
            "status",
            "failed"
        )

        return run_failed(
            runtime_error
        )


    def step(self,user_input):

        context = self.context_builder.build(
            user_input,
            self.state,
            self.memory.get_memory(),
            self.llm_tools_context
        )

        messages = self.prompt_builder.build(
            context
        )

        response = self.llm.chat(
            messages
        )

        self.trace.add_step(
            "llm_response",
            response
        )

        return response


    def handle_action(self,response):

        action = response["action"]

        if action == "final":

            answer = response["answer"]

            self.trace.add_step(
                "final_answer",
                answer
            )

            return answer


        if action == "tool":

            result = self.execute_tool(
                response
            )

            self.state.append_context(
                "tool_results",
                result
            )

            return None


    def execute_tool(self,response):

        tool_name = response["tool"]
        args = response["args"]

        return self.executor.execute(
            tool_name,
            **args
        )


    def update_memory(self,role,content):

        self.memory.add_memory(
            role,
            content
        )


    def update_state(self,key,value):

        self.state.update(
            key,
            value
        )