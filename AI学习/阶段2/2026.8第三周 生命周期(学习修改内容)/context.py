class ContextBuilder:

    def build(self,user_input,state,memory,tools_context):
        context = {
            "user_input":user_input,
            "state":state.to_context(),
            "memory":memory,
            "tools":tools_context
        }
        return context