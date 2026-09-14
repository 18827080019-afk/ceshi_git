from response import success, error
from models.tool import Tool
def add(a, b):
        try:
            result = a + b
            return success("add", {"a": a, "b": b}, result)
        except Exception as e:
            return error("add", {"a": a, "b": b}, str(e))

def multiply(a, b):
        try:
            result = a * b
            return success("multiply", {"a": a, "b": b}, result)
        except Exception as e:
            return error("multiply", {"a": a, "b": b}, str(e))

def upper(text):
        try:
            return success("upper", {"text": text}, text.upper())
        except Exception as e:
            return error("upper", {"text": text}, str(e))
        

def read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return error("read_file", {"path": path}, str(e))


#建立实例给LLm看
add_tool=Tool("add", "两个数的加法", add,schema={

"type":"object",

"properties":{

    "a":{
        "type":"number",
        "description":"第一个数字"
    },

    "b":{
        "type":"number",
        "description":"第二个数字"
    }

},

"required":[
    "a",
    "b"
]

})
multiply_tool=Tool("multiply", "两个数的乘法", multiply, schema={
    "type":"object",
    "properties":{
        "a":{
            "type":"number",
            "description":"第一个数字"
        },
        "b":{
            "type":"number",
            "description":"第二个数字"
        }
    },
    "required":[
        "a",
        "b"
    ]})
upper_tool=Tool("upper", "转换为大写", upper, schema={
    "type":"object",
    "properties":{
        "text":{
            "type":"string",
            "description":"要转换的文本"
        }
    },
    "required":[
        "text"
    ]
})
read_file_tool=Tool("read_file", "读取文件",read_file, schema={
    "type":"object",
    "properties":{
        "path":{
            "type":"string",
            "description":"文件路径"
        }
    },
    "required":[
        "path"
    ]
})