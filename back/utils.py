import jwt
from flask import abort, request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from conf import JWT_SECRET_KEY

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

def check_member() -> bool:
    check_token()
    jwt_token = request.headers.get('Authorization').split()[1]
    return jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms='HS512')['isMember']

def member_required(route):
    def wrapper(*args, **kwargs):
        if not check_member():
            abort(403, "Member rights are required")
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper

def check_admin() -> bool:
    check_token()
    jwt_token = request.headers.get('Authorization').split()[1]
    return jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms='HS512')['isAdmin']

def admin_required(route):
    def wrapper(*args, **kwargs):
        if not check_admin():
            abort(403, "Admin rights are required")
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper

def token_protected(route):
    def wrapper(*args, **kwargs):
        check_token()
        return route(*args, **kwargs)
    wrapper.__name__ = route.__name__
    return wrapper
