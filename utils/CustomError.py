class CustomError(Exception):
    # "Custom Exception class"
    def __init__(self, message="An error accured"):
        self.message = message
        super().__init__(self.message)
