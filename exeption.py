import logging


logging.basicConfig(level=logging.ERROR)


def read_file(file):
    try:
        with open(file) as f:
            f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


print(read_file("exeptions.txt"))
