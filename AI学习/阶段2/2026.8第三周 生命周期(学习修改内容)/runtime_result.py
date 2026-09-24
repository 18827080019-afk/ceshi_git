def run_success(answer):

    return {
        "status":"success",
        "answer":answer,
        "error":None
    }


def run_failed(error):

    return {
        "status":"failed",
        "answer":None,
        "error":error
    }