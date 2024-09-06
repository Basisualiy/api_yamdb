from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from .serializer import SignUpSerializer, TokenSerializator

User = get_user_model()


def get_confirmation_code(email, username):
    """Генерируем код подтверждения из логина и email."""
    return str(hash(email + username))[1:9]


class SignUpViewSet(APIView):
    """Регистрируем пользователя и высылаем ему код подтверждения."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            username = request.data.get('username')
        except KeyError:
            raise exceptions.ValidationError('Неверный запрос.',
                                             code=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(
            username=username,
            email=email)
        if not user.exists():
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(
                username=username,
                email=email)
        else:
            user = user[0]
        confirmation_code = get_confirmation_code(email, username)
        user.set_password(confirmation_code)
        user.save()
        send_mail(username,
                  f'Ваш код подтверждения: {confirmation_code}',
                  settings.SERVER_EMAIL,
                  [email, ],
                  fail_silently=False,)
        return Response(request.data,
                        status=status.HTTP_200_OK)


class TokenApiView(APIView):
    """Авторизуем пользователя и выдаем токен."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data.get('username'))
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response({'confirmation_code': str(token.access_token)},
                        status=status.HTTP_201_CREATED)
