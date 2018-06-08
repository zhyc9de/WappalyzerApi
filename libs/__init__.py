import os


def get_root_path(sub='/'):
    path = os.path.split(os.path.realpath(__file__))[0]
    return os.path.realpath(path + '/../' + sub) + '/'