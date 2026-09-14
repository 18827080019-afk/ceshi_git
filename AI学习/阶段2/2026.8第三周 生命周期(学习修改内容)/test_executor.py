#可学习检查结构
from executor import Executor
from models.register import Registry
from tool_functions import multiply_tool
from trace import Trace

registry = Registry()
registry.register(multiply_tool)

trace = Trace()

executor = Executor(
    registry,
    trace
)

print("正常参数：")
print(
    executor.execute(
        "multiply",
        a=8,
        b=7
    )
)

print("\n错误参数：")
print(
    executor.execute(
        "multiply",
        a=8,
        c=7
    )
)

print("\n不存在工具：")
print(
    executor.execute(
        "not_exist",
        a=8
    )
)