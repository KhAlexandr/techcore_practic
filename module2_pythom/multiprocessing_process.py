from multiprocessing import Process


def task():
    print(sum(range(100_000_000)))


if __name__ == "__main__":
    t = Process(target=task)
    t.start()
