import uuid
from datetime import datetime


class Trace:

    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.steps = []


    def add_step(self, step_type, data):

        step = {
            "time": datetime.now().isoformat(),
            "type": step_type,
            "data": data
        }
        self.steps.append(step)


    def get_trace(self):

        return {
            "trace_id": self.trace_id,
            "steps": self.steps
        }