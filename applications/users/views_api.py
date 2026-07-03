from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdmin


class UsuarioListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        usuarios = User.objects.filter(is_superuser=False)
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)


class UsuarioDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser:
                return None
            return user
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(usuario)
        return Response(serializer.data)


class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            occupation=serializer.validated_data.get('occupation', User.CLIENTE),
            gender=serializer.validated_data['gender'],
            date_birth=serializer.validated_data.get('date_birth'),
            phone=serializer.validated_data.get('phone', ''),
        )
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
