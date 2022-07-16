def payload_path_join(*args):
    joined_args = os.path.dirname(__file__) + os.sep + os.sep.join(args)
    return joined_args
    