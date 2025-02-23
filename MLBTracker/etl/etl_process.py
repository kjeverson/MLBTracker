import json
import requests
import datetime
from MLBTracker.models.player import Player
from MLBTracker.models.statistics import Batting, Pitching
from MLBTracker.models.team import Team


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
		Batting.objects.update_or_create(
			player=player,
			year=entry['year'],
			league=entry['league'],
			team=entry["org_abbreviation"],
			defaults={
				'plate_appearances': entry['plate_appearances'],
				'at_bats': entry['at_bats'],
				'games': entry['games'],
				'games_started': entry['games_started'],
				'runs': entry['runs'],
				'hits': entry['hits'],
				'doubles': entry['doubles'],
				'triples': entry['triples'],
				'home_runs': entry['home_runs'],
				'bases_on_balls': entry['bases_on_balls'],
				'strikeouts': entry['strikeouts'],
				'sacrifices': entry['sacrifices'],
				'sacrifice_flies': entry['sacrifice_flies'],
				'stolen_bases': entry['stolen_bases'],
				'caught_stealing': entry['caught_stealing']
			}
		)


def import_pitching_stats(player, pitching_stats):
	for entry in pitching_stats:
		try:
			Pitching.objects.update_or_create(
				player=player,
				year=entry["year"],
				league=entry["league"],
				team=entry["org_abbreviation"],
				defaults={
					'games': entry["games"],
					'games_started': entry["games_started"],
					'complete_games': entry["complete_games"],
					'games_finished': entry["games_finished"],
					'innings_pitched': entry["innings_pitched"],
					'wins': entry["wins"],
					'losses': entry["losses"],
					'saves': entry["saves"],
					'total_batters_faced': entry["total_batters_faced"],
					'at_bats': entry["at_bats"],
					'hits': entry["hits"],
					'doubles': entry["doubles"],
					'triples': entry["triples"],
					'home_runs': entry["home_runs"],
					'bases_on_balls': entry["bases_on_balls"],
					'strikeouts': entry["strikeouts"]
				}
			)
		except Exception as e:
			print(e)


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
			print(e)

	print(f"Imported {len(data)} players into the database.")





