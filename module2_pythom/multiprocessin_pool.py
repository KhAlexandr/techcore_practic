from multiprocessing import Pool


def tasks(x):
    return x * x


if __name__ == "__main__":
    nums = [n for n in range(1, 11)]
    with Pool(processes=8) as pool:
        result = pool.map(tasks, nums)
        print(result)
