import jwt
from flask import abort, request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from conf import JWT_SECRET_KEY


def token_protected(route):
    def wrapper(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if not authorization:
            abort(401, f"No Authentication method provided")
        method = authorization.split()[0]
        if method != "Bearer":
            abort(400, f"Authorization method '{method}' is not supported, use 'Bearer'")
        if len(authorization.split()) != 2:
            abort(400, f"No token provided for 'Bearer' authorization method")
        jwt_token = authorization.split()[1]
        try:
            request.data = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms='HS512')
        except ExpiredSignatureError:
            abort(498, "Token expired")
        except InvalidTokenError:
            abort(400, "Token is tampered")
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper
