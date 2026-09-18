class State:

    def __init__(self):
        self.data = {
            "task": None,
            "status": "idle",
            "context": {}
        }


    def update(self,key,value):
        self.data[key] = value

        
    def update_context(self,key,value):
        self.data["context"][key] = value


    def get(self):
        return self.data

    def to_context(self):#显示给后台看
        return {
        "status":self.data["status"],
        "context":self.data["context"]
    }


    def append_context(self,key,value):
        if key not in self.data["context"]:
            self.data["context"][key] = []
        self.data["context"][key].append(value)