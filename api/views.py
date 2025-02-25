from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from MLBTracker.models.player import Player
from MLBTracker.models.statistics import Batting, Pitching
from .serializers import PlayerListSerializer, BattingStatsSerializer, PitchingStatsSerializer


class PlayerListCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerListSerializer


class BattingStatsByYearView(APIView):
    def get(self, request, year):
        print(year)
        stats = get_list_or_404(Batting.objects.exclude(team='TOT'), year=year)
        serializer = BattingStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PitchingStatsByYearView(APIView):
    def get(self, request, year):
        stats = get_list_or_404(Pitching.objects.exclude(team='TOT'), year=year)
        serializer = PitchingStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
