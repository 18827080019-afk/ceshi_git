def success(tool,input,output):

    return {
        "tool":tool,
        "status":"success",
        "input":input,
        "output":output,
        "error":None
    }



def error(tool,input,message):

    return {
        "tool":tool,
        "status":"error",
        "input":input,
        "output":None,
        "error":message
    }