class DestinyAPIError(Exception):
    def __init__(self, errorCode):
        self.errorCode = errorCode
