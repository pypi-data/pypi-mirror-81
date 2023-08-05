import binascii
import os
from base64 import b64decode
from functools import wraps
from typing import Dict, Text, Tuple, Union

from sanic import response as r
from sanic_jwt import exceptions

from gino_admin import config
from gino_admin.utils import logger

cfg = config.cfg


def token_validation():
    def decorator(route):
        @wraps(route)
        async def validate(request, *args, **kwargs):
            if not os.getenv("ADMIN_AUTH_DISABLE") == "1":
                if (
                    not request.cookies
                    or not request.cookies.get("auth-token")
                    or request.cookies.get("auth-token") not in cfg.sessions
                    or (
                        request.cookies["auth-token"] in cfg.sessions
                        and cfg.sessions[request.cookies["auth-token"]]["user_agent"]
                        != request.headers["User-Agent"]
                    )
                ):
                    return r.redirect(f"{cfg.route}/login")
                else:
                    request["session"] = {"_auth": True}
                    return await route(request, *args, **kwargs)
            else:
                request["session"] = {"_auth": True}
                return await route(request, *args, **kwargs)

        return validate

    return decorator


def validate_login(request, _config):
    if request.method == "POST":
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        admin_user = str(_config["ADMIN_USER"])
        admin_password = str(_config["ADMIN_PASSWORD"])
        if username == admin_user and password == admin_password:
            return username
    return False


def logout_user(request):
    if request.cookies["auth-token"] in cfg.sessions:
        del cfg.sessions[request.cookies["auth-token"]]
    request.cookies["auth-token"] = None
    return request


async def authenticate(request, *args, **kwargs):
    if not os.getenv("ADMIN_AUTH_DISABLE") == "1":
        if "Basic" in request.token:
            username, password = user_credentials_from_the_token(request.token)
        else:
            username, password = request.token.split(":")

        if not username or not password:
            raise exceptions.AuthenticationFailed("Missing username or password.")

        user_in_cfg = str(cfg.app.config["ADMIN_USER"])
        password_in_cfg = str(cfg.app.config["ADMIN_PASSWORD"])

        if username != user_in_cfg:
            raise exceptions.AuthenticationFailed("User not found.")

        if password != password_in_cfg:
            raise exceptions.AuthenticationFailed("Password is incorrect.")

        return {"user_id": 1, "username": username}
    else:
        return {"user_id": 1, "username": "admin_no_auth"}


def user_credentials_from_the_token(token: Union[Text, bytes]) -> Union[Dict, Tuple]:
    """ decode base64 token to get pass and user_id """

    if not token:
        return {"error": "Need to provide Basic token"}

    token = token.split("Basic ")

    if len(token) == 2:
        decoded_token = token[1]
    else:
        return {
            "error": "Invalid data in Basic token. Token must starts with 'Basic ' "
        }
    try:
        decoded_token = b64decode(decoded_token).decode("utf-8")
    except (UnicodeDecodeError, binascii.Error) as e:
        return {
            "error": "Invalid data in Basic token. Codec can't decode bytes. Error message:"
            f"{e.args}"
        }

    if ":" not in decoded_token:
        return {
            "error": "Invalid data in Basic token, token str before encoding must follow format user:password"
            f"You sent: {decoded_token}"
        }

    first_semicolon = decoded_token.index(":")
    user_id = decoded_token[:first_semicolon]
    password = decoded_token[(first_semicolon + 1) :]  # noqa E203
    logger.debug(f"User decoded from Basic token: '{user_id}'")
    return user_id, password
