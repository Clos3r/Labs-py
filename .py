def calc(expr):
    expr = expr.replace(' ', '')

    while '(' in expr:
        start = expr.rfind('(')
        end = expr.find(')', start)
        inside = expr[start + 1:end]
        value = calc(inside)
        expr = expr[:start] + str(value) + expr[end + 1:]



    for op in ('*', '/'):
        parts = expr.split(op)
        if len(parts) > 1:
            left = calc(parts[0])
            right = calc(op.join(parts[1:]))
            return left * right if op == '*' else left / right

    for op in ('+', '-'):
        parts = expr.split(op)
        if len(parts) > 1:
            left = calc(parts[0])
            right = calc(op.join(parts[1:]))
            return left + right if op == '+' else left - right

    return float(expr)
