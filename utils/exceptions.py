class WrongTypeFieldException(Exception):
    def __init__(self, field:str, *args):
        super(Exception, self).__init__(*args)
        self.field = field
