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

    def to_context(self):
        return {
        "task":self.data["task"],
        "status":self.data["status"],
        "context":self.data["context"]
    }