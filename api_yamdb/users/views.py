from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminOnly
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOnly]
        return [permission() for permission in permission_classes]
