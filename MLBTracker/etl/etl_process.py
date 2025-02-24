import json
import requests
import datetime
from MLBTracker.models.player import Player
from MLBTracker.models.statistics import Batting, Pitching
from MLBTracker.models.team import Team
from MLBTracker.etl.statistic_functions import batting, pitching


def get_team_data():
	url = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/seasons/2025/teams?lang=en&region=us&limit=30"
	response = requests.get(url)
	team_data = response.json()['items']

	teams_data = []
	for team in team_data:
		teams_data.append(requests.get(team['$ref']).json())

	return teams_data


def import_mlb_teams(team_data):
	for entry in team_data:

		change_abrv = ["ARI", "CHW"]

		abbreviation = entry["abbreviation"]
		if abbreviation in change_abrv:
			if abbreviation == "ARI":
				abbreviation = "AZ"
			if abbreviation == "CHW":
				abbreviation = "CWS"

		team, created = Team.objects.get_or_create(
			id=abbreviation,
			location=entry["location"],
			name=entry["name"],
			full_name=entry["displayName"],
			primary_color="#" + entry["color"],
			secondary_color="#" + entry["alternateColor"]
		)


def load_json_data(file_path):
	with open(file_path, "r") as file:
		return json.load(file)


def import_batting_stats(player, batting_stats):
	for entry in batting_stats:

		at_bats = entry.get("at_bats", 0)
		hits = entry.get('hits', 0)
		doubles = entry.get('doubles', 0)
		triples = entry.get('triples', 0)
		home_runs = entry.get('home_runs', 0)
		strikeouts = entry.get('strikeouts', 0)
		sacrifice_flies = entry.get('sacrifice_flies', 0)

		singles = batting.calculate_singles(hits, doubles, triples, home_runs)
		batting_average = batting.calculate_batting_average(hits, at_bats)
		slugging_percentage = batting.calculate_slugging_percentage(singles, doubles, triples,
																	home_runs, at_bats)
		batting_balls_in_play = batting.calculate_batting_balls_in_play(hits, home_runs, at_bats,
																		strikeouts, sacrifice_flies)

		Batting.objects.update_or_create(
			player=player,
			year=entry['year'],
			league=entry['league'],
			team=entry["org_abbreviation"],
			defaults={
				'plate_appearances': entry.get('plate_appearances'),
				'at_bats': at_bats,
				'games': entry.get('games'),
				'games_started': entry.get('games_started'),
				'runs': entry.get('runs'),
				'hits': hits,
				'singles': singles,
				'doubles': doubles,
				'triples': triples,
				'home_runs': home_runs,
				'bases_on_balls': entry.get('bases_on_balls'),
				'strikeouts': strikeouts,
				'sacrifices': entry.get('sacrifices'),
				'sacrifice_flies': sacrifice_flies,
				'stolen_bases': entry.get('stolen_bases'),
				'caught_stealing': entry.get('caught_stealing'),
				'batting_average': batting_average,
				'slugging_percentage': slugging_percentage,
				'batting_balls_in_play': batting_balls_in_play
			}
		)


def import_pitching_stats(player, pitching_stats):
	for entry in pitching_stats:

		at_bats = entry.get('at_bats', 0)
		hits = entry.get('hits', 0)
		walks = entry.get('bases_on_balls', 0)
		innings_pitched = entry.get('innings_pitched', 0)
		wins = entry.get('wins', 0)
		losses = entry.get('losses', 0)
		strikeouts = entry.get('strikeouts', 0)

		batting_average = batting.calculate_batting_average(hits, at_bats)
		whip = pitching.calculate_whip(hits, walks, innings_pitched)
		win_percentage = pitching.calculate_win_percentage(wins, losses)
		k9 = pitching.calculate_k9(strikeouts, innings_pitched)
		bb9 = pitching.calculate_bb9(walks, innings_pitched)

		Pitching.objects.update_or_create(
			player=player,
			year=entry["year"],
			league=entry["league"],
			team=entry["org_abbreviation"],
			defaults={
				'games': entry.get("games"),
				'games_started': entry.get("games_started"),
				'complete_games': entry.get("complete_games"),
				'games_finished': entry.get("games_finished"),
				'innings_pitched': innings_pitched,
				'wins': wins,
				'losses': losses,
				'saves': entry.get("saves"),
				'total_batters_faced': entry.get("total_batters_faced"),
				'at_bats': at_bats,
				'hits': hits,
				'doubles': entry.get("doubles"),
				'triples': entry.get("triples"),
				'home_runs': entry.get("home_runs"),
				'bases_on_balls': walks,
				'strikeouts': strikeouts,
				'batting_average': batting_average,
				'whip': whip,
				'win_percentage': win_percentage,
				'k9': k9,
				'bb9': bb9
			}
		)


def import_data(data):
	for entry in data:
		team_key = entry["team"]
		team = Team.objects.get(pk=team_key)

		birthdate = datetime.datetime.strptime(entry["birth_date"], "%Y-%m-%d").date()

		try:
			player, created = Player.objects.get_or_create(
				id=entry["id"],
				name_first=entry["name_first"],
				name_use=entry["name_use"],
				name_last=entry["name_last"],
				name_short=entry["name_first"][0] + ". " + entry["name_last"],
				name_full=entry["name_first"] + " " + entry["name_last"],
				team=team,
				birth_date=birthdate,
				height_feet=entry["height_feet"],
				height_inches=entry.get("height_inches"),
				weight=entry["weight"],
				throws=entry["throws"],
				bats=entry["bats"],
				primary_position=entry.get("primary_position"),
				secondary_position=entry.get("secondary_position")
			)

			if not created:
				player.team = team
				player.primary_position = entry.get('primary_position')
				player.secondary_position = entry.get('secondary_position')
				player.weight = entry['weight']
				player.height_feet = entry['height_feet']
				player.height_inches = entry.get("height_inches")
				player.save()

			batting = entry['stats']['batting']
			pitching = entry['stats']['pitching']

			if batting:
				import_batting_stats(player, batting)

			if pitching:
				import_pitching_stats(player, pitching)

		except Exception as e:
			print(e, player.name_full)

	print(f"Imported {len(data)} players into the database.")





