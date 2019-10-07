from datetime import datetime

import jwt
from django.conf import settings

from api.services import BaseService


class Token(BaseService):

    @staticmethod
    def get_header():
        return {
            "alg": "HS256",
            "typ": "JWT"
        }

    @staticmethod
    def get_secret_key():
        return settings.SECRET_KEY

    @staticmethod
    def encode(user):
        payload = {
            "username": user.username,
            "iat": datetime.now().timestamp()
        }
        token = jwt.encode(payload, Token.get_secret_key(), algorithm='HS256')
        return token.decode("utf-8")
