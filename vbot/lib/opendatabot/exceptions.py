class OpendatabotBaseError(Exception):
    pass


class OpendatabotClientError(OpendatabotBaseError):
    pass


class OpendatabotTimeoutError(OpendatabotBaseError):
    pass


class OpendatabotServiceError(OpendatabotBaseError):
    pass


class OpendatabotNotFoundError(OpendatabotBaseError):
    pass
