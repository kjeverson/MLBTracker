from django.db import models
from .player import Player


class Batting(models.Model):
	id = models.BigAutoField(primary_key=True)
	player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting')	
	year = models.IntegerField(null=False)
	league = models.CharField(max_length=2, null=True, blank=True)
	team = models.CharField(max_length=3, null=False)
	teams = models.IntegerField(null=False, default=1)

	plate_appearances = models.IntegerField(null=False, default=0)
	at_bats = models.IntegerField(null=False, default=0)
	games = models.IntegerField(null=False, default=0)
	games_started = models.IntegerField(null=False, default=0)
	runs = models.IntegerField(null=False, default=0)
	hits = models.IntegerField(null=False, default=0)
	singles = models.IntegerField(null=False, default=0)
	doubles = models.IntegerField(null=False, default=0)
	triples = models.IntegerField(null=False, default=0)
	home_runs = models.IntegerField(null=False, default=0)
	bases_on_balls = models.IntegerField(null=False, default=0)
	strikeouts = models.IntegerField(null=False, default=0)
	sacrifices = models.IntegerField(null=False, default=0)
	sacrifice_flies = models.IntegerField(null=False, default=0)
	stolen_bases = models.IntegerField(null=False, default=0)
	caught_stealing = models.IntegerField(null=False, default=0)

	batting_average = models.DecimalField(max_digits=4, decimal_places=3, default=0)
	slugging_percentage = models.DecimalField(max_digits=4, decimal_places=3, default=0)
	batting_balls_in_play = models.DecimalField(max_digits=4, decimal_places=3, default=0)

	def __str__(self):
		return f"{self.player.name_full} - {self.year}"


class Pitching(models.Model):
	id = models.BigAutoField(primary_key=True)
	player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pitching')
	year = models.IntegerField(null=False)
	league = models.CharField(max_length=2, null=True, blank=True)
	team = models.CharField(max_length=3, null=False)
	teams = models.IntegerField(null=False, default=1)

	games = models.IntegerField(null=False, default=0)
	games_started = models.IntegerField(null=False, default=0)
	complete_games = models.IntegerField(null=False, default=0)
	games_finished = models.IntegerField(null=False, default=0)
	innings = models.IntegerField(null=False, default=0)
	innings_outs = models.IntegerField(null=False, default=0)
	wins = models.IntegerField(null=False, default=0)
	losses = models.IntegerField(null=False, default=0)
	saves = models.IntegerField(null=False, default=0)
	total_batters_faced = models.IntegerField(null=False, default=0)
	at_bats = models.IntegerField(null=False, default=0)
	hits = models.IntegerField(null=False, default=0)
	doubles = models.IntegerField(null=False, default=0)
	triples = models.IntegerField(null=False, default=0)
	home_runs = models.IntegerField(null=False, default=0)
	bases_on_balls = models.IntegerField(null=False, default=0)
	strikeouts = models.IntegerField(null=False, default=0)

	batting_average = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	whip = models.DecimalField(max_digits=5, decimal_places=3, default=0)
	win_percentage = models.DecimalField(max_digits=4, decimal_places=3, default=0)
	k9 = models.DecimalField(max_digits=6, decimal_places=3, default=0)
	bb9 = models.DecimalField(max_digits=6, decimal_places=3, default=0)

	def __str__(self):
		return f"{self.player.name_full} - {self.year}"

	def innings_pitched(self):
		innings, outs = divmod(self.innings_outs, 3)
		total_innings = self.innings + innings
		return float(f'{total_innings}.{outs}')
