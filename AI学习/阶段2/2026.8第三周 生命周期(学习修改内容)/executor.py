
from response import success, error

class Executor:

    def __init__(self, registry,trace):      #将Registry类的实例化对象传入Executor类,用于执行工具-->registry初始化的接收传入形参
        self.registry = registry         #excutor=Executor(registry)
        self.trace = trace


    def execute(self, tool_name,**arguments):
        # 1. 查找工具
        self.trace.add_step("tool_call",{ "tool":tool_name,"arguments":arguments})
        tool = self.registry.get(tool_name)

        # 2. 判断工具是否存在
        if tool is None:
            error_result=error(tool_name, arguments, f"tool not found: {tool_name}")
            self.trace.add_step("tool_result",error_result)  #工具调用错误也要被trace记录
            return error_result#自设错误边界
               
    
        schema = tool.schema

        #3. 检查参数是否符合工具的schema,参数是否传对
        properties = tool.schema.get("properties",{})  #获取字典的键对应的值,若无对应返回{}
        
        for key in arguments:  #拿字典的键,  
            if key not in properties:
                error_result=error(tool_name,arguments,f"unknown parameter:{key}")
                self.trace.add_step("tool_result",error_result)
                return error_result 
            
        #4检查是否缺少参数
        required = schema.get("required",[])

        for key in required:
            if key not in arguments:
                error_result = error(tool_name,arguments,f"missing required parameter:{key}")
                self.trace.add_step("tool_result",error_result)

                return error_result

        #预设应有的数据类型
        type_map = {"number": (int,float),"string": str}     

        #5检查输入数据类型是否正确*************************************************8
        
        for key,value in arguments.items():
            expected_type = properties[key].get("type")
            python_type = type_map.get(expected_type)

            if expected_type == "number":

                if isinstance(value,bool) or not isinstance(value,(int,float)):
                    error_result = error(tool_name,arguments,f"invalid type:{key}, expected number")
                    self.trace.add_step("tool_result",error_result)

                    return error_result
                
            elif python_type is not None: #第一层,符合预设数据类型
                if not isinstance(value,python_type): #第二层,符合arguments数据类型

                    error_result = error(tool_name,arguments,f"invalid type:{key}, expected {expected_type}")
                    self.trace.add_step("tool_result",error_result)

                    return error_result
            else:
  
                error_result = error(tool_name,arguments,f"unsupported schema type:{expected_type}")
                self.trace.add_step("tool_result",error_result)

                return error_result  

            #################invalid type= Schema认识这个类型，但用户传错了 unsupported schema type= Executor自己还不支持Schema声明的类型
        # 执行工具
        try:
            result = tool.run(**arguments)
            result_success=success(tool_name,arguments,result)
            self.trace.add_step("tool_result",result_success)
            return result_success
        # 4. 捕获错误
        except Exception as e:
            error_result = error(tool_name,arguments,str(e))
       
            self.trace.add_step("tool_result",error_result)
            return error_result
                    
                        