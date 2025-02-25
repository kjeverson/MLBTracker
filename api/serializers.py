from rest_framework import serializers
from MLBTracker.models.player import Player
from MLBTracker.models.team import Team
from MLBTracker.models.statistics import Batting, Pitching


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class PlayerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name_short", "get_primary_position"]


class PlayerListSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Player
        fields = ["id", "name_full",
                  "primary_position", "get_primary_position",
                  "secondary_position", "get_secondary_position",
                  "team"]


class BattingStatsSerializer(serializers.ModelSerializer):
    player = PlayerShortSerializer()

    class Meta:
        model = Batting
        unique_together = ('player', 'year', 'league', 'team')
        ordering = ['-year', 'player']
        fields = '__all__'


class PitchingStatsSerializer(serializers.ModelSerializer):
    player = PlayerShortSerializer()
    innings_pitched = serializers.SerializerMethodField()

    class Meta:
        model = Pitching
        unique_together = ('player', 'year', 'league', 'team')
        ordering = ['-year', 'player']
        fields = '__all__'

    def get_innings_pitched(self, obj):
        # Call the innings_pitched method from your model instance (obj)
        return obj.innings_pitched()
