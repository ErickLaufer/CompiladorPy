def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    elif hasattr(node, '__dict__'):
        print(f"{prefix}{node.__class__.__name__}")
        for key, value in node.__dict__.items():
            print(f"{prefix}  {key}:")
            print_ast(value, indent + 2)
    else:
        print(f"{prefix}{node}")
