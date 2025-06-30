import re

class RiscVGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code.splitlines()
        self.asm = []
        self.register_map = {}
        self.reg_count = 0
        self.vars = set()

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

            if re.match(r'^L\d+:$', line):
                self.asm.append(line)
                continue

            if line.startswith("if "):
                cond_var = re.findall(r"if (t\d+) goto (L\d+)", line)[0]
                reg = self.new_reg(cond_var[0])
                self.asm.append(f"    la t6, {cond_var[0]}")
                self.asm.append(f"    lw t6, 0(t6)")
                self.asm.append(f"    bne t6, zero, {cond_var[1]}")
                continue

            if line.startswith("goto "):
                label = line.split()[1]
                self.asm.append(f"    j {label}")
                continue

            if "=" in line:
                dest, expr = map(str.strip, line.split("=", 1))

                if expr.startswith("call"):
                    call_match = re.match(r"call (\w+)\((.*)\)", expr)
                    func_name = call_match.group(1)
                    args = [arg.strip() for arg in call_match.group(2).split(",") if arg.strip()]

                    for i, arg in enumerate(args):
                        if arg.isdigit():
                            self.asm.append(f"    li a{i}, {arg}")
                        else:
                            self.asm.append(f"    la t6, {arg}")
                            self.asm.append(f"    lw a{i}, 0(t6)")

                    self.asm.append(f"    jal {func_name}")
                    self.asm.append(f"    la t6, {dest}")
                    self.asm.append(f"    sw a0, 0(t6)")
                    continue

                if any(op in expr for op in ["+", "-", "*", "/", ">", "<", ">=", "<=", "==", "!="]):
                    tokens = expr.split()
                    a, op, b = tokens[0], tokens[1], tokens[2]
                    ra = self.new_reg(a)
                    rb = self.new_reg(b)
                    rd = self.new_reg(dest)

                    if a.isdigit():
                        self.asm.append(f"    li {ra}, {a}")
                    else:
                        self.asm.append(f"    la t6, {a}")
                        self.asm.append(f"    lw {ra}, 0(t6)")

                    if b.isdigit():
                        self.asm.append(f"    li {rb}, {b}")
                    else:
                        self.asm.append(f"    la t6, {b}")
                        self.asm.append(f"    lw {rb}, 0(t6)")

                    instr_map = {
                        '+': 'add',
                        '-': 'sub',
                        '*': 'mul',
                        '/': 'div',
                        '>': 'sgt',
                        '<': 'slt',
                        '>=': 'sge',
                        '<=': 'sle',
                        '==': 'seqz',
                        '!=': 'snez'
                    }

                    instr = instr_map.get(op)
                    if instr:
                        self.asm.append(f"    {instr} {rd}, {ra}, {rb}")
                        self.asm.append(f"    la t6, {dest}")
                        self.asm.append(f"    sw {rd}, 0(t6)")
                    continue

                elif expr.isdigit():
                    reg = self.new_reg(dest)
                    self.asm.append(f"    li {reg}, {expr}")
                    self.asm.append(f"    la t6, {dest}")
                    self.asm.append(f"    sw {reg}, 0(t6)")
                else:
                    src_reg = self.new_reg(expr)
                    self.asm.append(f"    la t6, {expr}")
                    self.asm.append(f"    lw {src_reg}, 0(t6)")
                    self.asm.append(f"    la t6, {dest}")
                    self.asm.append(f"    sw {src_reg}, 0(t6)")

        self.asm.append("    li a7, 10")
        self.asm.append("    ecall")
        return "\n".join(self.asm)

    def _collect_vars(self):
        for line in self.tac_code:
            if "=" in line and not line.strip().startswith("t") and not line.strip().startswith("if"):
                var = line.split("=")[0].strip()
                self.vars.add(var)

        # incluir temporários
        for line in self.tac_code:
            matches = re.findall(r"\bt\d+\b", line)
            for match in matches:
                self.vars.add(match)