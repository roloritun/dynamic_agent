from langchain.tools import Tool
from database import BuiltinTool

def create_builtin_tools(session):
    builtin_tools = session.query(BuiltinTool).all()
    tools = []
    
    for tool in builtin_tools:
        # Create the function with security validation
        def secure_function(query, tool=tool):
            # Security check: Validate API key (or any other required credentials)
            required_key = tool.required_api_key
            provided_key = query.get('api_key')

            if required_key and provided_key != required_key:
                return "Unauthorized: Invalid API key."

            # Dynamically execute the function code if the security check passes
            exec(tool.function_code, globals())
            return globals()[tool.name](query.get('input', ''))

        # Create the tool with the secure function
        secure_tool = Tool(
            name=tool.name,
            func=secure_function,
            description=tool.description
        )
        tools.append(secure_tool)
    
    return tools
