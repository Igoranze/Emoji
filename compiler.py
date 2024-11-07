#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

import argparse

class EmojicodeCompiler:
    def __init__(self, code=None, file_path=None):
        self.code = code
        self.file_path = file_path
        self.transpiled_code = ""

        self.python_indents = 0

        if self.file_path:
            self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                # only read .emoji files
                if not self.file_path.endswith('.emoji'):
                    print("File must be a .emoji file.")
                    return

                self.code = file.read()
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            self.code = ""

    def get_python_indents_string(self):
        return "    " * self.python_indents if self.python_indents > 0 else ""

    def transpile_line(self, line):
        result = self.get_python_indents_string()

        line = line.strip()
        if not line:
            return ""

        if line.startswith('🤡'):
            return  self.get_python_indents_string() + f"# {line[2:]}\n"

        if line.startswith('👎'):
            self.python_indents -= 1
            return ""

        if re.match(r'🤖 \w+ ✏️', line):
            var, value = re.findall(r'🤖 (\w+) ✏️ (.+)', line)[0]
            var = var.strip()
            value = value.strip()
            result += f"{var} = {value}\n"

        elif line.startswith('🖨'):
            var = line[2:].strip()
            result += f"print({var})\n"

        elif line.startswith("🤔"):
            condition = line[1:].replace("👍", "").strip()
            expr1, expr2 = re.findall(r'(\w+) ✅️ (.+)', condition)[0]
            result += f"{self.transpiled_operator(expr2, if_statement=True, expected_valuer=expr1)}:\n"
            self.python_indents += 1

        elif "➕" in line or "➖" in line or "✖️" in line or  "➗" in line or "➿" in line:
            result += self.transpiled_operator(line)


        elif line.startswith('🔁'):
            condition = line[1:].replace("👍", "").strip()
            result += f"while {condition}:\n"
            self.python_indents += 1

        return result

    def transpiled_operator(self, line, if_statement=False, expected_valuer=None):
        result = ""

        if "➕" in line:
            expr1, expr2 = re.findall(r'(\w+) ➕️(.+)', line)[0]
            operator = "+"
        elif "➖" in line:
            expr1, expr2 = re.findall(r'(\w+) ➖(.+)', line)[0]
            operator = "-"
        elif "✖️" in line:
            expr1, expr2 = re.findall(r'(\w+) ✖️(.+)', line)[0]
            operator = "*"
        elif "➗" in line:
            expr1, expr2 = re.findall(r'(\w+) ➗️(.+)', line)[0]
            operator = "/"
        elif "➿" in line:
            expr1, expr2 = re.findall(r'(\w+) ➿(.+)', line)[0]
            operator = "%"
        else:
            return f"if {line} == {expected_valuer}"

        if expr1 and expr2 and operator:
            if if_statement and expected_valuer:
                result = f"if {expr1} {operator} {expr2} == {expected_valuer}"
            else:
                result = f"{expr1} = {expr1} {operator} {expr2}"

        return result

    def transpile(self):
        lines = self.code.splitlines()

        for line in lines:
            line_result = self.transpile_line(line)
            self.transpiled_code += line_result

    def execute(self):
        try:
            exec(self.transpiled_code)
        except Exception as e:
            print(f"Failed to exec: {e}")

def main():
    parser = argparse.ArgumentParser(description="Compile .emoji to Python code.")
    parser.add_argument('file', metavar='file', type=str, help="Path to the .emoji file.")

    args = parser.parse_args()

    compiler = EmojicodeCompiler(file_path=args.file)
    compiler.transpile()
    # print(compiler.transpiled_code)
    compiler.execute()

if __name__ == "__main__":
    main()
