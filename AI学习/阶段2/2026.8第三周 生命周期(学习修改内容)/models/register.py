class Registry:        #register为基础实例

    def __init__(self):
        # 保存所有工具
        self.tools = {}


    def register(self, tool):            #-->与class Tool的实例化对象绑定,注册工具
        # 注册工具
        self.tools[tool.name] = tool


    def get(self, name):
        # 获取工具
        return self.tools.get(name)


    def get_all_tools(self):
        # 获取所有工具描述信息
        return self.tools.values()

# registry=Registry()
# registry.register(#登记的实例对象(元数据))
#  eg   (multiply_tool)
