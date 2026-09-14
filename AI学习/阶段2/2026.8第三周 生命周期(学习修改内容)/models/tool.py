
class Tool:

    def __init__(
        self,
        name,
        description,
        func,
        schema
        
    ):
        self.name=name
        self.description=description
        self.schema=schema
        self.func=func


    def run(self,*args,**kwargs):
            return self.func(*args,**kwargs)
    
    def get_info(self):
            return {
                "name":self.name,
                "description":self.description,
                "parameters":self.schema

            }

#eg:创建实例:add_tool=Tool("add", "两个数的加法", {"a":"number", "b":"number"},add)
