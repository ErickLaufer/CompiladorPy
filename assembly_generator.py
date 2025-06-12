class AssemblyGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code.splitlines()
        self.assembly = []

    def generate(self):
        for line in self.tac_code:
            line = line.strip()

            if not line:
                continue

            if line.startswith("func"):
                self.assembly.append(f"{line.split()[1]}:")
            elif line == "end":
                self.assembly.append("RET")
            elif line.startswith("return "):
                value = line.split(" ", 1)[1]
                self.assembly.append(f"MOV R0, {value}")
                self.assembly.append("RET")
            elif " = call " in line:
                # Ex: t1 = call soma(a, b)
                temp, rest = line.split(" = ")
                func_call = rest.replace("call ", "")
                name, args = func_call.split("(", 1)
                args = args.strip(")").split(", ")
                for i, arg in enumerate(args):
                    self.assembly.append(f"MOV ARG{i}, {arg}")
                self.assembly.append(f"CALL {name}")
                self.assembly.append(f"MOV {temp}, R0")
            elif "=" in line:
                dest, expr = line.split(" = ")

                if any(op in expr for op in ['+', '-', '*', '/']):
                    a, op, b = expr.split()
                    self.assembly.append(f"MOV R1, {a}")
                    self.assembly.append(f"{op.upper()} R1, {b}")
                    self.assembly.append(f"MOV {dest}, R1")
                else:
                    self.assembly.append(f"MOV {dest}, {expr}")

        return "\n".join(self.assembly)
