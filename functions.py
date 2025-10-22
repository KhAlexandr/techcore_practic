def logger(message, *args, **kwargs):
    return f"{message} {args[0]}, {args[1]} инициализированы {kwargs['user']} - ом"


print(logger("Test", 1, 2, user="admin"))
