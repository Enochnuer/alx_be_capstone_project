from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Optionally restrict access

    def perform_create(self, serializer):
        # Automatically associate the profile with the logged-in user
        serializer.save(user=self.request.user)
