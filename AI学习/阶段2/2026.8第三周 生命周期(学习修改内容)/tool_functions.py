from response import success, error
from models.tool import Tool
def add(a, b):
            result = a + b
            return  result

def multiply(a, b):
            result = a * b
            return result

def upper(text):
            return text.upper()

def read_file(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

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