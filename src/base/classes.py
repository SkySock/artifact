from rest_framework import generics, permissions, mixins, decorators, viewsets


class ActionPermissionMixin:
    """
    Миксин permissions для action
    """
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ActionSerializerMixin:
    """
        Миксин serializers для action
    """
    serializer_class_by_action = None

    def get_serializer_class(self):
        try:
            return self.serializer_class_by_action[self.action]
        except KeyError:
            return self.serializer_class


class CreateRetrieveUpdateDestroy(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  ActionPermissionMixin,
                                  viewsets.GenericViewSet):
    """
    """
    pass
