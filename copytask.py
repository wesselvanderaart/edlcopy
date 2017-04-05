class copytask(object):

    src_file = None
    src_file_path = None
    src_file_size = None
    src_subtree = None
    dest_file_path = None
    dest_file = None

    def __init__(self, id, status="Not Found"):
        self.id = id
        self.status = status

class copytaskList(object):

    def __init__(self):
