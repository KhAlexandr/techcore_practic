def calc(a, b, op):

    if a.isalpha():
        a = str(a)
    elif "." in a:
        a = float(a)
    else:
        a = int(a)

    if b.isalpha():
        b = str(b)
    elif "." in b:
        b = float(b)
    else:
        b = int(b)

    if op == "+":
        return a + b
    if op == "*":
        return a * b
    if op == "-":
        return a - b
    if op == "/":
        if b == 0:
            return "Нельзя делить на ноль"
        return a / b


a = input("Введите первый аргумент:")
op = input("Введите символ(+, -, *, /):")
b = input("Введите второй аргумент:")


calc(a=a, b=b, op=op)
