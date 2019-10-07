from django.conf import settings
from django.contrib.auth.hashers import make_password

from api.services import BaseService


class UserService(BaseService):
    @staticmethod
    def get_creation_data(data, key):
        if data['role'] is  None or data['role'] == "":
            data['role'] = key
        data['password'] = make_password(data.get('password'), salt=settings.SECRET_KEY)
        return data
