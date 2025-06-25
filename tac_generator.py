from ast_nodes import *

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.generate(stmt)

        elif isinstance(node, VarDecl):
            result = self.generate(node.value)
            self.code.append(f"{node.identifier} = {result}")

        elif isinstance(node, Assignment):
            result = self.generate(node.value)
            self.code.append(f"{node.identifier} = {result}")

        elif isinstance(node, BinaryOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.op} {right}")
            return temp

        elif isinstance(node, Number):
            return str(node.value)

        elif isinstance(node, Float):
            return str(node.value)

        elif isinstance(node, String):
            return f'"{node.value}"'

        elif isinstance(node, Boolean):
            return "true" if node.value else "false"

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, FunctionCall):
            args = [self.generate(arg) for arg in node.arguments]
            temp = self.new_temp()
            self.code.append(f"{temp} = call {node.name}({', '.join(args)})")
            return temp

        elif isinstance(node, Return):
            result = self.generate(node.value)
            self.code.append(f"return {result}")

        elif isinstance(node, FunctionDecl):
            self.code.append(f"\nfunc {node.name}({', '.join(name for name, _ in node.parameters)}) -> {node.return_type}")
            for stmt in node.body:
                self.generate(stmt)
            self.code.append("end")
            
        elif isinstance(node, IfStatement):
            cond = self.generate(node.condition)
            l_true = self.new_label()
            l_false = self.new_label() if node.false_block else None
            l_end = self.new_label()

            self.code.append(f"if {cond} goto {l_true}")
            if l_false:
                self.code.append(f"goto {l_false}")
            else:
                self.code.append(f"goto {l_end}")

            self.code.append(f"{l_true}:")
            for stmt in node.true_block:
                self.generate(stmt)
            self.code.append(f"goto {l_end}")

            if node.false_block:
                self.code.append(f"{l_false}:")
                for stmt in node.false_block:
                    self.generate(stmt)

            self.code.append(f"{l_end}:")
        else:
            raise Exception(f"Nó desconhecido: {type(node)}")

    def dump(self):
        return "\n".join(self.code)
    
