class Protocol:
    
    def __init__(self):
        self.protocol_errors=[]


    def protocol_error_add(self,error,field,response):
        protocol_error= {
            "type": "protocol_error",
            "code": error,
            "message": f"{error}: {field}",
            "field": field,
            "recoverable": True,
            "response": response
        }
        self.protocol_errors.append(protocol_error)
    
       