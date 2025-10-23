def logger(message, *args, **kwargs):
    return f"{message} {args}инициализированы {kwargs} - ом"


print(logger("Test", 1, 2, user="admin"))
