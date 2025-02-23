from django.shortcuts import render
from rest_framework import generics
from MLBTracker.models.player import Player
from .serializers import PlayerListSerializer


class PlayerListCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerListSerializer

