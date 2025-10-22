def calc(a, b, op):
    a = float(a) if "." in a else int(a)
    b = float(b) if "." in b else int(b)

    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    return a / b


a = input("Введите первый аргумент:")
op = input("Введите символ(+, -, *, /):")
b = input("Введите второй аргумент:")


calc(a=a, b=b, op=op)
