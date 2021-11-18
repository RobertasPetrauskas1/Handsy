import time

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import handsy
from jwt import PyJWTError



def decode_jwt(token: str):
    settings = handsy.get_settings()
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["exp", "iss", "aud", "iat", "uname", "uid", "urole"]},
        leeway=settings.jwt_leeway,
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def encode_jwt(user_id: str, user_name: str, role):
    settings = handsy.get_settings()
    payload = {
        "uid": user_id,
        "uname": user_name,
        "urole": role,
        "iat": time.time(),
        "exp": time.time() + 6000000,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


class JWTBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            try:
                jwt_payload: dict = decode_jwt(credentials.credentials)
                request.state.jwt_payload = jwt_payload
                return jwt_payload
            except PyJWTError:
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def __eq__(self, other):
        return isinstance(other, JWTBearer)

    def __hash__(self):
        return 1290959922195836047
