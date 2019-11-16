from datetime import datetime

import jwt
from django.conf import settings

from api.models import User
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

    @staticmethod
    def decode(token):
        token_hours = 1
        try:
            payload = jwt.decode(token, Token.get_secret_key(), algorithms=['HS256'])

            iat = int(payload.get("iat"))
            username = payload.get('username')

            if iat + token_hours * 60 * 60 < datetime.now().timestamp():
                return None

            user = User.objects.get(username=username)
        except:
            return None
        return user
