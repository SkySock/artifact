from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from base.permissions import IsOptions
from .serializers import TelegramAuthSerializer, UserDetailSerializer, TelegramAuthResponseSerializer
from .services.telegram import check_telegram_auth


@extend_schema(
        request=TelegramAuthSerializer,
        responses=TelegramAuthResponseSerializer,
    )
@api_view(['POST'])
def telegram_auth(request):
    serializer_class = TelegramAuthSerializer
    serializer_data = serializer_class(data=request.data)
    if serializer_data.is_valid():
        token = check_telegram_auth(serializer_data)
        return Response(token, status=status.HTTP_200_OK)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data telegram')


class CheckAuthMe(RetrieveAPIView):
    permission_classes = (IsAuthenticated | IsOptions,)
    serializer_class = UserDetailSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj
