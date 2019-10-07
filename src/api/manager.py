from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have an password")
        user_obj = self.model()
        user_obj.set_password(password)  # change user password
        user_obj.save(using=self._db)
        return user_obj
