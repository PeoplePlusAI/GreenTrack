def read_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return content
