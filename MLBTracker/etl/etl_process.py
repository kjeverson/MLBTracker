import json
import requests
import datetime
from collections import defaultdict
from django.db.models import Sum
from MLBTracker.models.player import Player
from MLBTracker.models.statistics import Batting, Pitching
from MLBTracker.models.team import Team
from MLBTracker.etl.statistic_functions import batting, pitching


def get_team_data():
	url = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/seasons/2025/teams?" \
		  "lang=en&region=us&limit=30"
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


def aggregate_career_batting_stats(player):
	stats = player.batting.all().exclude(team='OVR').order_by('-year')

	if not stats.exists():
		return

	latest = stats.first()

	career_batting_stats = stats.aggregate(
		teams=Sum('teams') or 0,
		plate_appearances=Sum('plate_appearances') or 0,
		at_bats=Sum('at_bats') or 0,
		games=Sum('games') or 0,
		games_started=Sum('games_started') or 0,
		runs=Sum('runs') or 0,
		hits=Sum('hits') or 0,
		singles=Sum('singles') or 0,
		doubles=Sum('doubles') or 0,
		triples=Sum('triples') or 0,
		home_runs=Sum('home_runs') or 0,
		bases_on_balls=Sum('bases_on_balls') or 0,
		strikeouts=Sum('strikeouts') or 0,
		sacrifices=Sum('sacrifices') or 0,
		sacrifice_flies=Sum('sacrifice_flies') or 0,
		stolen_bases=Sum('stolen_bases') or 0,
		caught_stealing=Sum('caught_stealing') or 0
	)

	batting_average = batting.calculate_batting_average(
		career_batting_stats['hits'], career_batting_stats['at_bats'])
	slugging_percentage = batting.calculate_slugging_percentage(
		career_batting_stats['singles'], career_batting_stats['doubles'],
		career_batting_stats['triples'], career_batting_stats['home_runs'],
		career_batting_stats['at_bats'])
	batting_balls_in_play = batting.calculate_batting_balls_in_play(
		career_batting_stats['hits'], career_batting_stats['home_runs'],
		career_batting_stats['at_bats'], career_batting_stats['strikeouts'],
		career_batting_stats['sacrifice_flies'])

	Batting.objects.update_or_create(
		player=player,
		year=latest.year,
		league=None,
		team="TOT",
		teams=career_batting_stats['teams'],
		defaults={
			'plate_appearances': career_batting_stats["plate_appearances"],
			'at_bats': career_batting_stats["at_bats"],
			'games': career_batting_stats["games"],
			'games_started': career_batting_stats["games_started"],
			'runs': career_batting_stats["runs"],
			'hits': career_batting_stats["hits"],
			'singles': career_batting_stats["singles"],
			'doubles': career_batting_stats["doubles"],
			'triples': career_batting_stats["triples"],
			'home_runs': career_batting_stats["home_runs"],
			'bases_on_balls': career_batting_stats["bases_on_balls"],
			'strikeouts': career_batting_stats["strikeouts"],
			'sacrifices': career_batting_stats["sacrifices"],
			'sacrifice_flies': career_batting_stats["sacrifice_flies"],
			'stolen_bases': career_batting_stats["stolen_bases"],
			'caught_stealing': career_batting_stats["caught_stealing"],
			'batting_average': batting_average,
			'slugging_percentage': slugging_percentage,
			'batting_balls_in_play': batting_balls_in_play
		}
	)


def aggregate_batting_stats(player, yearly_entries):
	duplicate_years = [key for key, entries in yearly_entries.items() if len(entries) > 1]

	for year in duplicate_years:
		aggregated_stats = Batting.objects.filter(player=player, year=year).aggregate(
			total_teams=Sum("teams"),
			total_plate_appearances=Sum("plate_appearances") or 0,
			total_at_bats=Sum("at_bats") or 0,
			total_games=Sum("games") or 0,
			total_games_started=Sum("games_started") or 0,
			total_runs=Sum("runs") or 0,
			total_hits=Sum("hits") or 0,
			total_singles=Sum("singles") or 0,
			total_doubles=Sum("doubles") or 0,
			total_triples=Sum("triples") or 0,
			total_home_runs=Sum("home_runs") or 0,
			total_bases_on_balls=Sum("bases_on_balls") or 0,
			total_strikeouts=Sum("strikeouts") or 0,
			total_sacrifices=Sum("sacrifices") or 0,
			total_sacrifice_flies=Sum("sacrifice_flies") or 0,
			total_stolen_bases=Sum("stolen_bases") or 0,
			total_caught_stealing=Sum("caught_stealing") or 0
		)

		# Calculated stats for aggregated season stats
		batting_average = batting.calculate_batting_average(
			aggregated_stats["total_hits"], aggregated_stats["total_at_bats"])
		slugging_percentage = batting.calculate_slugging_percentage(
			aggregated_stats["total_singles"], aggregated_stats["total_doubles"],
			aggregated_stats["total_triples"], aggregated_stats["total_home_runs"],
			aggregated_stats["total_at_bats"])
		batting_balls_in_play = batting.calculate_batting_balls_in_play(
			aggregated_stats["total_hits"], aggregated_stats["total_home_runs"],
			aggregated_stats["total_at_bats"], aggregated_stats["total_strikeouts"],
			aggregated_stats["total_sacrifice_flies"])

		Batting.objects.update_or_create(
			player=player,
			year=year,
			league=None,
			team="OVR",
			teams=aggregated_stats["total_teams"],
			defaults={
				'plate_appearances': aggregated_stats["total_plate_appearances"],
				'at_bats': aggregated_stats["total_at_bats"],
				'games': aggregated_stats["total_games"],
				'games_started': aggregated_stats["total_games_started"],
				'runs': aggregated_stats["total_runs"],
				'hits': aggregated_stats["total_hits"],
				'singles': aggregated_stats["total_singles"],
				'doubles': aggregated_stats["total_doubles"],
				'triples': aggregated_stats["total_triples"],
				'home_runs': aggregated_stats["total_home_runs"],
				'bases_on_balls': aggregated_stats["total_bases_on_balls"],
				'strikeouts': aggregated_stats["total_strikeouts"],
				'sacrifices': aggregated_stats["total_sacrifices"],
				'sacrifice_flies': aggregated_stats["total_sacrifice_flies"],
				'stolen_bases': aggregated_stats["total_stolen_bases"],
				'caught_stealing': aggregated_stats["total_caught_stealing"],
				'batting_average': batting_average,
				'slugging_percentage': slugging_percentage,
				'batting_balls_in_play': batting_balls_in_play
			}
		)


def import_batting_stats(player, batting_stats):
	yearly_entries = defaultdict(list)

	for entry in batting_stats:

		# Skip Aggregated Seasons, as we re-aggregate later
		if entry['org_abbreviation'] == 'OVR':
			continue

		year = entry['year']
		yearly_entries[year].append(entry)

		at_bats = entry.get("at_bats", 0)
		hits = entry.get('hits', 0)
		doubles = entry.get('doubles', 0)
		triples = entry.get('triples', 0)
		home_runs = entry.get('home_runs', 0)
		strikeouts = entry.get('strikeouts', 0)
		sacrifice_flies = entry.get('sacrifice_flies', 0)

		singles = batting.calculate_singles(hits, doubles, triples, home_runs)
		batting_average = batting.calculate_batting_average(hits, at_bats)
		slugging_percentage = batting.calculate_slugging_percentage(
			singles, doubles, triples, home_runs, at_bats)
		batting_balls_in_play = batting.calculate_batting_balls_in_play(
			hits, home_runs, at_bats, strikeouts, sacrifice_flies)

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

	aggregate_batting_stats(player, yearly_entries)
	aggregate_career_batting_stats(player)


def aggregate_career_pitching_stats(player):
	stats = player.pitching.all().exclude(team='OVR').order_by('-year')
	if not stats.exists():
		return

	latest = stats.first()

	aggregated_stats = stats.aggregate(
		total_teams=Sum("teams"),
		total_games=Sum("games") or 0,
		total_games_started=Sum("games_started") or 0,
		total_complete_games=Sum("complete_games") or 0,
		total_games_finished=Sum("games_finished") or 0,
		total_innings=Sum("innings") or 0,
		total_innings_outs=Sum("innings_outs") or 0,
		total_wins=Sum("wins") or 0,
		total_losses=Sum("losses") or 0,
		total_saves=Sum("saves") or 0,
		total_batters_faced=Sum("total_batters_faced") or 0,
		total_at_bats=Sum("at_bats") or 0,
		total_hits=Sum("hits") or 0,
		total_doubles=Sum("doubles") or 0,
		total_triples=Sum("triples") or 0,
		total_home_runs=Sum("home_runs") or 0,
		total_bases_on_balls=Sum("bases_on_balls") or 0,
		total_strikeouts=Sum("strikeouts") or 0,
	)

	# Calculated stats for aggregated season stats
	total_innings_pitched = pitching.get_innings_pitched(
		aggregated_stats['total_innings'], aggregated_stats['total_innings_outs'])

	batting_average = batting.calculate_batting_average(
		aggregated_stats["total_hits"], aggregated_stats["total_at_bats"])
	whip = pitching.calculate_whip(
		aggregated_stats['total_hits'], aggregated_stats['total_bases_on_balls'],
		total_innings_pitched)
	win_percentage = pitching.calculate_win_percentage(
		aggregated_stats['total_wins'], aggregated_stats['total_losses'])
	k9 = pitching.calculate_k9(
		aggregated_stats['total_strikeouts'], total_innings_pitched)
	bb9 = pitching.calculate_bb9(
		aggregated_stats['total_bases_on_balls'], total_innings_pitched)

	Pitching.objects.update_or_create(
		player=player,
		year=latest.year,
		league=None,
		team="TOT",
		teams=aggregated_stats["total_teams"],
		defaults={
			"games": aggregated_stats["total_games"],
			"games_started": aggregated_stats["total_games_started"],
			"complete_games": aggregated_stats["total_complete_games"],
			"games_finished": aggregated_stats["total_games_finished"],
			"innings": aggregated_stats["total_innings"],
			"innings_outs": aggregated_stats["total_innings_outs"],
			"wins": aggregated_stats["total_wins"],
			"losses": aggregated_stats["total_losses"],
			"saves": aggregated_stats["total_saves"],
			"total_batters_faced": aggregated_stats["total_batters_faced"],
			"at_bats": aggregated_stats["total_at_bats"],
			"hits": aggregated_stats["total_hits"],
			"doubles": aggregated_stats["total_doubles"],
			"triples": aggregated_stats["total_triples"],
			"home_runs": aggregated_stats["total_home_runs"],
			"bases_on_balls": aggregated_stats["total_bases_on_balls"],
			"strikeouts": aggregated_stats["total_strikeouts"],
			"batting_average": batting_average,
			"whip": whip,
			"win_percentage": win_percentage,
			"k9": k9,
			"bb9": bb9
		},
	)


def aggregate_pitching_stats(player, yearly_entries):
	duplicate_years = [key for key, entries in yearly_entries.items() if len(entries) > 1]

	for year in duplicate_years:
		aggregated_stats = Pitching.objects.filter(player=player, year=year).aggregate(
			total_teams=Sum("teams"),
			total_games=Sum("games") or 0,
			total_games_started=Sum("games_started") or 0,
			total_complete_games=Sum("complete_games") or 0,
			total_games_finished=Sum("games_finished") or 0,
			total_innings=Sum("innings") or 0,
			total_innings_outs=Sum("innings_outs") or 0,
			total_wins=Sum("wins") or 0,
			total_losses=Sum("losses") or 0,
			total_saves=Sum("saves") or 0,
			total_batters_faced=Sum("total_batters_faced") or 0,
			total_at_bats=Sum("at_bats") or 0,
			total_hits=Sum("hits") or 0,
			total_doubles=Sum("doubles") or 0,
			total_triples=Sum("triples") or 0,
			total_home_runs=Sum("home_runs") or 0,
			total_bases_on_balls=Sum("bases_on_balls") or 0,
			total_strikeouts=Sum("strikeouts") or 0,
		)

		# Calculated stats for aggregated season stats
		total_innings_pitched = pitching.get_innings_pitched(
			aggregated_stats['total_innings'], aggregated_stats['total_innings_outs'])

		batting_average = batting.calculate_batting_average(
			aggregated_stats["total_hits"], aggregated_stats["total_at_bats"])
		whip = pitching.calculate_whip(
			aggregated_stats['total_hits'], aggregated_stats['total_bases_on_balls'],
			total_innings_pitched)
		win_percentage = pitching.calculate_win_percentage(
			aggregated_stats['total_wins'], aggregated_stats['total_losses'])
		k9 = pitching.calculate_k9(
			aggregated_stats['total_strikeouts'], total_innings_pitched)
		bb9 = pitching.calculate_bb9(
			aggregated_stats['total_bases_on_balls'], total_innings_pitched)

		Pitching.objects.update_or_create(
			player=player,
			year=year,
			league=None,
			team="OVR",
			teams=aggregated_stats["total_teams"],
			defaults={
				"games": aggregated_stats["total_games"],
				"games_started": aggregated_stats["total_games_started"],
				"complete_games": aggregated_stats["total_complete_games"],
				"games_finished": aggregated_stats["total_games_finished"],
				"innings": aggregated_stats["total_innings"],
				"innings_outs": aggregated_stats["total_innings_outs"],
				"wins": aggregated_stats["total_wins"],
				"losses": aggregated_stats["total_losses"],
				"saves": aggregated_stats["total_saves"],
				"total_batters_faced": aggregated_stats["total_batters_faced"],
				"at_bats": aggregated_stats["total_at_bats"],
				"hits": aggregated_stats["total_hits"],
				"doubles": aggregated_stats["total_doubles"],
				"triples": aggregated_stats["total_triples"],
				"home_runs": aggregated_stats["total_home_runs"],
				"bases_on_balls": aggregated_stats["total_bases_on_balls"],
				"strikeouts": aggregated_stats["total_strikeouts"],
				"batting_average": batting_average,
				"whip": whip,
				"win_percentage": win_percentage,
				"k9": k9,
				"bb9": bb9
			},
		)


def import_pitching_stats(player, pitching_stats):
	yearly_entries = defaultdict(list)

	for entry in pitching_stats:

		# Skip Aggregated Seasons, as we re-aggregate later
		if entry['org_abbreviation'] == 'OVR':
			continue

		year = entry['year']
		yearly_entries[year].append(entry)

		at_bats = entry.get('at_bats', 0)
		hits = entry.get('hits', 0)
		walks = entry.get('bases_on_balls', 0)
		innings, innings_outs = str(entry.get('innings_pitched')).split(".")
		wins = entry.get('wins', 0)
		losses = entry.get('losses', 0)
		strikeouts = entry.get('strikeouts', 0)

		innings_pitched = pitching.get_innings_pitched(innings, innings_outs)

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
				'teams': 1,
				'games': entry.get("games"),
				'games_started': entry.get("games_started"),
				'complete_games': entry.get("complete_games"),
				'games_finished': entry.get("games_finished"),
				'innings': innings,
				'innings_outs': innings_outs,
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

	aggregate_pitching_stats(player, yearly_entries)
	aggregate_career_pitching_stats(player)


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

			batting_entries = entry['stats']['batting']
			pitching_entries = entry['stats']['pitching']

			if batting_entries:
				import_batting_stats(player, batting_entries)

			if pitching_entries:
				import_pitching_stats(player, pitching_entries)

		except Exception as e:
			print(f"Error processing player {player.name_full}: {e}")

	print(f"Imported {len(data)} players into the database.")





