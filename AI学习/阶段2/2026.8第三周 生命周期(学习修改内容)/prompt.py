class PromptBuilder:

    def build(self,context):

        system_prompt = f"""
你是一个Agent。记住你只能进行以下操作(只能用我提供的工具计算结果,不能自己计算),不要输出你的多余思考:
如果需要工具:
返回:
{{
"action":"tool",
"tool":"工具名称",
"args":{{}}
}}
如果完成:
返回:
{{
"action":"final",
"answer":"回答"
}}
当前状态:
{context["state"]}
可用工具:
{context["tools"]}

"""
       
        messages = [
            {
                "role":"system",
                "content":system_prompt
            }
        ]

        messages.extend(
            context["memory"]
        )

        messages.append(
            {
                "role":"user",
                "content":context["user_input"]
            }
        )

        return messages