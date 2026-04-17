import os

# Tokenizer
def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        c = expr[i]

        if c.isspace():
            i += 1
            continue

        if c.isdigit() or c == '.':
            start = i
            dot_count = 0

            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        return None
                i += 1

            tokens.append(("NUM", expr[start:i]))
            continue

        if c in '+-*/':
            tokens.append(("OP", c))
            i += 1
            continue

        if c == '(':
            tokens.append(("LPAREN", c))
            i += 1
            continue

        if c == ')':
            tokens.append(("RPAREN", c))
            i += 1
            continue

        return None  # invalid character

    tokens.append(("END", ""))
    return tokens


# Parser

def parse(tokens):
    pos = 0

    def peek():
        return tokens[pos]

    def consume(expected_type=None, expected_value=None):
        nonlocal pos
        tok = tokens[pos]

        if expected_type and tok[0] != expected_type:
            raise Exception()

        if expected_value and tok[1] != expected_value:
            raise Exception()

        pos += 1
        return tok

    def parse_expression():
        node = parse_term()

        while peek()[0] == "OP" and peek()[1] in ('+', '-'):
            op = consume("OP")[1]
            right = parse_term()
            node = ("bin", op, node, right)

        return node

    def parse_term():
        node = parse_factor()

        while True:
            tok = peek()

            # explicit * or /
            if tok[0] == "OP" and tok[1] in ('*', '/'):
                op = consume("OP")[1]
                right = parse_factor()
                node = ("bin", op, node, right)

            # implicit multiplication
            elif tok[0] in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("bin", '*', node, right)

            else:
                break

        return node

    def parse_factor():
        tok = peek()

        if tok[0] == "OP" and tok[1] == '-':
            consume("OP")
            operand = parse_factor()
            return ("neg", operand)

        if tok[0] == "OP" and tok[1] == '+':
            raise Exception()  # unary + not allowed

        return parse_primary()

    def parse_primary():
        tok = peek()

        if tok[0] == "NUM":
            consume("NUM")
            return ("num", float(tok[1]))

        if tok[0] == "LPAREN":
            consume("LPAREN")
            node = parse_expression()

            if peek()[0] != "RPAREN":
                raise Exception()

            consume("RPAREN")
            return node

        raise Exception()

    tree = parse_expression()

    if peek()[0] != "END":
        raise Exception()

    return tree


# Tree Formatting

def format_tree(node):
    kind = node[0]

    if kind == "num":
        val = node[1]
        return str(int(val)) if val.is_integer() else str(val)

    if kind == "neg":
        return f"(neg {format_tree(node[1])})"

    if kind == "bin":
        _, op, left, right = node
        return f"({op} {format_tree(left)} {format_tree(right)})"


# Evaluation

def evaluate(node):
    kind = node[0]

    if kind == "num":
        return node[1]

    if kind == "neg":
        return -evaluate(node[1])

    if kind == "bin":
        _, op, left, right = node
        l = evaluate(left)
        r = evaluate(right)

        if op == '+':
            return l + r
        if op == '-':
            return l - r
        if op == '*':
            return l * r
        if op == '/':
            if r == 0:
                raise Exception()
            return l / r


# Token Formatting

def format_tokens(tokens):
    parts = []
    for ttype, value in tokens:
        if ttype == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{ttype}:{value}]")
    return " ".join(parts)


# ---------------------------
# Result Formatting
# ---------------------------

def format_result(val):
    return str(int(val)) if val.is_integer() else f"{val:.4f}"


# main

def evaluate_file(input_path: str):
    results = []
    output_lines = []

    with open(input_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        expr = line.rstrip("\n")

        entry = {
            "input": expr,
            "tree": "",
            "tokens": "",
            "result": ""
        }

        # Parsing Phase
        try:
            tokens = tokenize(expr)
            if tokens is None:
                raise Exception()

            token_str = format_tokens(tokens)
            tree = parse(tokens)
            tree_str = format_tree(tree)

        except Exception:
            entry["tree"] = "ERROR"
            entry["tokens"] = "ERROR"
            entry["result"] = "ERROR"

            results.append(entry)

            output_lines.extend([
                f"Input: {expr}",
                "Tree: ERROR",
                "Tokens: ERROR",
                "Result: ERROR",
                ""
            ])
            continue

        # Evaluation Phase
        try:
            value = evaluate(tree)
            result_value = value
            result_str = format_result(value)
        except Exception:
            result_value = "ERROR"
            result_str = "ERROR"

        entry["tree"] = tree_str
        entry["tokens"] = token_str
        entry["result"] = result_value

        results.append(entry)

        output_lines.extend([
            f"Input: {expr}",
            f"Tree: {tree_str}",
            f"Tokens: {token_str}",
            f"Result: {result_str}",
            ""
        ])

    # Write output file
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(output_path, "w") as f:
        f.write("\n".join(output_lines).rstrip() + "\n")

    return results



# Optional Runner

if __name__ == "__main__":
    print("Mathematical Expression Evaluator")

    input_file = "sample_input.txt"

    # Check if file exists
    if not os.path.exists(input_file):
        print(f" Error: Input file '{input_file}' not found.")
        print("👉 Make sure the file exists in the current directory.")
    else:
        try:
            print(f"Reading input from: {input_file}")
            results = evaluate_file(input_file)

            print("Processing complete.")
            print("Output written to 'output.txt' in the same directory.")



        except Exception as e:
            print("Unexpected error occurred while processing the file.")
            print(f"Details: {e}")