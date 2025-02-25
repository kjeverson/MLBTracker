from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from MLBTracker.models.player import Player
from MLBTracker.models.statistics import Batting, Pitching


def players(request):
	return render(request, 'players.html')


@require_GET
def get_player_modal(request, player_id):
	player = Player.objects.get(id=player_id)

	batting_stats = player.batting.all().exclude(team='TOT').order_by('-year')
	pitching_stats = player.pitching.all().exclude(team='TOT').order_by('-year')

	context = {
		'player': player,
		'batting_stats': batting_stats,
		"pitching_stats": pitching_stats,
		'career_batting_stats': player.batting.filter(team='TOT').first(),
		'career_pitching_stats': player.pitching.filter(team='TOT').first(),
		'current_pitching_stats': pitching_stats.first(),
		'current_batting_stats': batting_stats.first(),
		'aggregated_pitching_years': player.get_aggregated_years(pitching=True),
		'aggregated_batting_years': player.get_aggregated_years(pitching=False)
	}

	modal = render_to_string('modals/playerModal.html', context)
	return JsonResponse({'html': modal})


def batting(request):
	years = list(Batting.objects.all()
				 .order_by('-year')
				 .values_list('year', flat=True)
				 .distinct())

	context = {
		'years': years
	}
	return render(request, 'batting_stats.html', context)


def pitching(request):
	years = list(Pitching.objects.all()
				 .order_by('-year')
				 .values_list('year', flat=True)
				 .distinct())

	context = {
		'years': years
	}

	return render(request, 'pitching_stats.html', context)