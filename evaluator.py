# ===== Vinh: TOKENIZER + PARSER =====

def tokenize(expression):
    tokens = []
    index = 0

    while index < len(expression):
        character = expression[index]

        if character.isspace():
            index += 1
            continue

        if character in "0123456789":
            start = index

            while (
                index < len(expression)
                and expression[index] in "0123456789"
            ):
                index += 1

            if index < len(expression) and expression[index] == ".":
                index += 1
                decimal_start = index

                while (
                    index < len(expression)
                    and expression[index] in "0123456789"
                ):
                    index += 1

                if index == decimal_start:
                    raise ValueError("Invalid number")

            tokens.append(("NUM", expression[start:index]))
            continue

        if character in "+-*/%^":
            tokens.append(("OP", character))
            index += 1
            continue

        if character == "(":
            tokens.append(("LPAREN", "("))
            index += 1
            continue

        if character == ")":
            tokens.append(("RPAREN", ")"))
            index += 1
            continue

        raise ValueError("Invalid character")

    tokens.append(("END", ""))
    return tokens 


def parse_primary(tokens, index):
    token_type, token_value = tokens[index]

    if token_type == "NUM":
        return ("num", token_value), index + 1

    if token_type == "LPAREN":
        tree, index = parse_expression(tokens, index + 1)

        if tokens[index][0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        return tree, index + 1

    raise ValueError("Expected number or opening parenthesis")


def parse_power(tokens, index):
    left, index = parse_primary(tokens, index)

    if tokens[index] == ("OP", "^"):
        right, index = parse_unary(tokens, index + 1)
        left = ("bin", "^", left, right)

    return left, index

def parse_unary(tokens, index):
    if tokens[index] == ("OP", "-"):
        child, index = parse_unary(tokens, index + 1)
        return ("neg", child), index

    return parse_power(tokens, index)

def parse_term(tokens, index):
    left, index = parse_unary(tokens, index)

    while True:
        current = tokens[index]

        if current[0] == "OP" and current[1] in "*/%":
            operator = current[1]
            right, index = parse_unary(tokens, index + 1)
            left = ("bin", operator, left, right)

        elif current[0] == "LPAREN":
            # Implicit multiplication: 2(3 + 4)
            right, index = parse_unary(tokens, index)
            left = ("bin", "*", left, right)

        elif (
            current[0] == "NUM"
            and index > 0
            and tokens[index - 1][0] == "RPAREN"
        ):
            # Implicit multiplication: (2 + 3)4
            right, index = parse_unary(tokens, index)
            left = ("bin", "*", left, right)

        else:
            break

    return left, index


def parse_expression(tokens, index):
    left, index = parse_term(tokens, index)

    while (
        tokens[index][0] == "OP"
        and tokens[index][1] in "+-"
    ):
        operator = tokens[index][1]
        right, index = parse_term(tokens, index + 1)
        left = ("bin", operator, left, right)

    return left, index

def parse(tokens):
    tree, index = parse_expression(tokens, 0)

    if tokens[index][0] != "END":
        raise ValueError("Unexpected token")

    return tree


# ===== Andy: EVALUATION + OUTPUT =====

import os


def evaluate_tree(tree):
    if tree[0] == "num":
        return float(tree[1])

    if tree[0] == "neg":
        return -evaluate_tree(tree[1])

    if tree[0] == "bin":
        left = evaluate_tree(tree[2])
        right = evaluate_tree(tree[3])
        operator = tree[1]

        if operator == "+":
            return left + right

        elif operator == "-":
            return left - right

        elif operator == "*":
            return left * right

        elif operator == "/":
            return left / right

        elif operator == "%":
            return left % right

        elif operator == "^":
            return left ** right


def tree_to_string(tree):
    if tree[0] == "num":
        return format_number(float(tree[1]))

    if tree[0] == "neg":
        child = tree_to_string(tree[1])
        return f"(neg {child})"

    if tree[0] == "bin":
        operator = tree[1]
        left = tree_to_string(tree[2])
        right = tree_to_string(tree[3])

        return f"({operator} {left} {right})"


def tokens_to_string(tokens):
    parts = []

    for token_type, token_value in tokens:
        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{token_value}]")

    return " ".join(parts)


def format_number(value):
    if value.is_integer():
        return str(int(value))

    return str(round(value, 4))


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    with open(input_path, "r") as file:
        expressions = file.read().splitlines()

    for expression in expressions:
        try:
            tokens = tokenize(expression)
            tree = parse(tokens)

            tree_text = tree_to_string(tree)
            token_text = tokens_to_string(tokens)

            try:
                value = evaluate_tree(tree)
                result_value = value

            except ArithmeticError:
                result_value = "ERROR"

        except (ValueError, IndexError):
            tree_text = "ERROR"
            token_text = "ERROR"
            result_value = "ERROR"

        results.append({
            "input": expression,
            "tree": tree_text,
            "tokens": token_text,
            "result": result_value
        })

    output_path = os.path.join(
        os.path.dirname(input_path),
        "output.txt"
    )

    with open(output_path, "w") as file:
        for result in results:
            file.write(f"Input: {result['input']}\n")
            file.write(f"Tree: {result['tree']}\n")
            file.write(f"Tokens: {result['tokens']}\n")

            if result["result"] == "ERROR":
                file.write("Result: ERROR\n")
            else:
                file.write(
                    f"Result: {format_number(result['result'])}\n"
                )

            file.write("\n")

    return results


if __name__ == "__main__":
    evaluate_file("input.txt")