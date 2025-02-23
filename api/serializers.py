from rest_framework import serializers
from MLBTracker.models.player import Player
from MLBTracker.models.team import Team
from MLBTracker.models.statistics import Batting, Pitching


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerListSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Player
        fields = ["id", "name_full",
                  "primary_position", "get_primary_position",
                  "secondary_position", "get_secondary_position",
                  "team"]


class BattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batting
        unique_together = ('player', 'year', 'league', 'team')
        ordering = ['-year', 'player']
        fields = '__all__'


class PitchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitching
        unique_together = ('player', 'year', 'league', 'team')
        ordering = ['-year', 'player']
        fields = '__all__'
