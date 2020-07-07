from flask import abort


class ErrorHandler:
    # TODO: add docstrings

    def __init__(self, subject, code=400,
                 msg="Oops, something went wrong..."):
        self.subject = subject
        self.code = code
        self.msg = msg

    @staticmethod
    def abort(code, msg, e=None):
        if e is not None:
            print(e)
        return abort(code, msg)

    @staticmethod
    def provide_parameters(code=400):
        msg = f"Please, provide all necessary parameters"
        return abort(code, msg)

    def custom_abort(self):
        return abort(self.code, self.msg)

    def not_exists(self, e=None, code=400):
        if e is not None:
            print(e)
        msg = f"{self.subject} doesn't exist"
        return abort(code, msg)

    def unable_to_update(self, e=None, code=500):
        if e is not None:
            print(e)
        msg = f"Unable to update {self.subject}"
        return abort(code, msg)

    def unable_to_create(self, e=None, code=500):
        if e is not None:
            print(e)
        msg = f"Unable to create new {self.subject}"
        return abort(code, msg)

    def unable_to_delete(self, e=None, code=500):
        if e is not None:
            print(e)
        msg = f"Unable to delete {self.subject}"
        return abort(code, msg)


error_plant = ErrorHandler('Plant')
error_book = ErrorHandler('Book')
error_user = ErrorHandler('User')
