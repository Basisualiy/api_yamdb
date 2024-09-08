import uuid


def get_confirmation_code(email, username):
    """Генерируем код подтверждения из логина и email."""
    return str(uuid.uuid3(uuid.NAMESPACE_DNS,
                          str(hash(email + username))[1:9]))


def check_confirmation_code(user, confirmation_code):
    return user.confirmation_code == confirmation_code
