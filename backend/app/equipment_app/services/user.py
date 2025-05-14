from django.contrib.auth.models import User
from django.db import IntegrityError, DataError
from rest_framework_simplejwt.tokens import RefreshToken


def register_user(username, password, email=None) -> User:
    if User.objects.filter(username=username).exists():
        raise ValueError('Username already exists')
    try:
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
    except IntegrityError:
        raise ValueError('Username already exists')
    except DataError as e:
        raise ValueError(str(e))
    return user


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }
