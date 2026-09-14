class Memory:
    def __init__(self):
        self.messages = []

    def add_memory(self,role,content):
        self.messages.append({
                "role":role,
                "content":content
            }
        )


    def get_memory(self):
        return self.messages


    def clear_memory(self):
        self.messages.clear()
