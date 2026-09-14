
from response import success, error

class Executor:

    def __init__(self, registry,trace):      #将Registry类的实例化对象传入Executor类,用于执行工具-->registry初始化的接收传入形参
        self.registry = registry         #excutor=Executor(registry)
        self.trace = trace


    def execute(self, tool_name,**arguments):
        # 1. 查找工具
        tool = self.registry.get(tool_name)

        # 2. 判断工具是否存在
        if tool is None:
            return error(tool_name, arguments, f"tool not found: {tool_name}") #自设错误边界
               
    
        schema = tool.schema
        properties = schema.get("properties",{})  #获取字典的键对应的值,若无对应返回{}

        #3. 检查参数是否符合工具的schema
        for key in arguments:  #拿字典的键  
            if key not in properties:
                return error(tool_name,arguments,f"unknown parameter:{key}") #

        self.trace.add_step("tool_call",{"tool": tool_name,"arguments": arguments})

        # 3. 执行工具
        try:
            result = tool.run(**arguments)
            self.trace.add_step("tool_result",result)
            return result

        # 4. 捕获错误
        except Exception as e:
            error_result = error(tool_name,arguments,str(e))
       
            self.trace.add_step("tool_result",error_result)
            return error_result
                    
                        