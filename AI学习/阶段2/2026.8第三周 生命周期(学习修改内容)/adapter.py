
def build_tool_context(registry):
    tools = []

    for tool in registry.get_all_tools():
        info = tool.get_info()
        tools.append(info)

    return tools