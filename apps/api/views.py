from rest_framework.views import APIView
from rest_framework import response, status
from django.contrib.auth import authenticate


from ..account.models import User
from .serializers import RegistrationSerializer, ProfileUpdateSerializer, ResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.validated_data, status=status.HTTP_202_ACCEPTED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.validated_data, status=status.HTTP_202_ACCEPTED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ResetPasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            user = authenticate(request=request, username=user.username, password=serializer.validated_data.get("password"))
            if user is not None:
                serializer.save()
                return response.Response(data=serializer.validated_data, status=status.HTTP_202_ACCEPTED)
            return response.Response(data={"password": ["wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        