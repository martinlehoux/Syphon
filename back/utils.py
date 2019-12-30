from hashlib import scrypt
import jwt
from flask import abort, request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from conf import JWT_SECRET_KEY, SCRYPT_SECRET_KEY

def check_token() -> bool:
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
    return True


def token_protected(route):
    def wrapper(*args, **kwargs):
        check_token()
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper

def hash_password(password: str) -> bytes:
    return scrypt(bytes(password, 'utf-8'), salt=SCRYPT_SECRET_KEY, n=1<<14, r=8, p=1)
