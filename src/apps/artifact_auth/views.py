from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import TelegramAuthSerializer
from .services.telegram import check_telegram_auth


@api_view(['POST'])
def telegram_auth(request):
    serializer_class = TelegramAuthSerializer
    serializer_data = serializer_class(data=request.data)
    if serializer_data.is_valid():
        token = check_telegram_auth(serializer_data)
        return Response(token, status=status.HTTP_200_OK)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data telegram')
