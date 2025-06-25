import re

class RiscVGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code.splitlines()
        self.asm = []
        self.register_map = {}
        self.reg_count = 0
        self.vars = set()
        self.in_function = False

    def new_reg(self, var):
        if var not in self.register_map:
            self.register_map[var] = f"t{self.reg_count}"
            self.reg_count = (self.reg_count + 1) % 7
        return self.register_map[var]

    def generate(self):
        self._collect_vars()

        self.asm.append(".data")
        for var in self.vars:
            self.asm.append(f"{var}: .word 0")

        self.asm.append("\n.text")
        self.asm.append("main:")

        for line in self.tac_code:
            line = line.strip()
            if not line:
                continue

            if line.startswith("func"):
                func_name = re.findall(r"func (\w+)", line)[0]
                self.asm.append(f"\n{func_name}:")
                self.in_function = True
                continue

            if line == "end":
                if self.in_function:
                    self.asm.append("    jr ra")
                    self.in_function = False
                continue

            if re.match(r'^L\d+:$', line):
                self.asm.append(line)
                continue

            if line.startswith("return "):
                value = line.replace("return ", "").strip()
                if value.isdigit():
                    self.asm.append(f"    li a0, {value}")
                else:
                    self.asm.append(f"    lw a0, {value}")
                continue

            if line.startswith("if "):
                cond_var, label = re.findall(r"if (\w+) goto (\w+)", line)[0]
                self.asm.append(f"    lw t6, {cond_var}")
                self.asm.append(f"    bne t6, zero, {label}")
                continue

            if line.startswith("goto "):
                label = line.split()[1]
                self.asm.append(f"    j {label}")
                continue

            if "=" in line:
                dest, expr = map(str.strip, line.split("=", 1))

                # chamada de função
                match_call = re.match(r'call (\w+)\((.*)\)', expr)
                if match_call:
                    func_name, args = match_call.groups()
                    args = [arg.strip() for arg in args.split(",")]
                    for i, arg in enumerate(args):
                        if arg.isdigit():
                            self.asm.append(f"    li a{i}, {arg}")
                        else:
                            self.asm.append(f"    lw a{i}, {arg}")
                    self.asm.append(f"    jal {func_name}")
                    self.asm.append(f"    sw a0, {dest}")
                    continue

                # expressão binária
                if any(op in expr for op in ["+", "-", "*", "/", ">", "<", ">=", "<=", "==", "!="]):
                    a, op, b = expr.split()
                    ra = self.new_reg(a)
                    rb = self.new_reg(b)
                    rd = self.new_reg(dest)

                    if a.isdigit():
                        self.asm.append(f"    li {ra}, {a}")
                    else:
                        self.asm.append(f"    lw {ra}, {a}")
                    if b.isdigit():
                        self.asm.append(f"    li {rb}, {b}")
                    else:
                        self.asm.append(f"    lw {rb}, {b}")

                    instr_map = {
                        '+': 'add',
                        '-': 'sub',
                        '*': 'mul',
                        '/': 'div',
                        '>': 'sgt',
                        '<': 'slt',
                        '>=': 'bge',  # cuidado: instruções booleanas podem mudar a lógica
                        '<=': 'ble',
                        '==': 'beq',
                        '!=': 'bne'
                    }

                    instr = instr_map.get(op, 'add')
                    self.asm.append(f"    {instr} {rd}, {ra}, {rb}")
                    self.asm.append(f"    sw {rd}, {dest}")
                    continue

                # atribuição direta
                if expr.isdigit():
                    reg = self.new_reg(dest)
                    self.asm.append(f"    li {reg}, {expr}")
                    self.asm.append(f"    sw {reg}, {dest}")
                else:
                    reg = self.new_reg(expr)
                    self.asm.append(f"    lw {reg}, {expr}")
                    self.asm.append(f"    sw {reg}, {dest}")

        self.asm.append("    li a7, 10")
        self.asm.append("    ecall")
        return "\n".join(self.asm)

    def _collect_vars(self):
        for line in self.tac_code:
            if "=" in line and not line.startswith("t") and not line.startswith("call"):
                var = line.split("=")[0].strip()
                self.vars.add(var)
