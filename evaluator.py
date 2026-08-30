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

def evaluate_tree(tree):
    pass


def tree_to_string(tree):
    pass


def tokens_to_string(tokens):
    pass


def format_number(value):
    pass


def evaluate_file(input_path: str) -> list[dict]:
    pass
