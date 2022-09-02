class CustomError(Exception):
    # base exception for ECOM related errors
    pass

class BadRequestError(CustomError):
    # exception for indicating incorrect request parameters 
    pass

class NotFoundError(CustomError):
    # exception when a resource is not found in the database
    pass

class UnauthorizedError(CustomError):
    # exception for unauthorized requests
    pass