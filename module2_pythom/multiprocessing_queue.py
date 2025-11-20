from multiprocessing import Process, Queue


def Producer(q):
    q.put(10)


def Consumer(q):
    print(q.get())


if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=Producer, args=(q,))
    p2 = Process(target=Consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
