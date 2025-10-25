def read_large_log(file_path):
    with open(file_path) as f:
        for line in f:
            yield line
