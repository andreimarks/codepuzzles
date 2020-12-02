def get_list_from_file(filename):
    with open(filename, "r") as file:
        return file.read().splitlines();