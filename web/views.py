from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.db.models import Sum
from MLBTracker.models.player import Player


def home(request):
	return render(request, 'index.html')


@require_GET
def get_player_modal(request, player_id):
	player = Player.objects.get(id=player_id)
	batting_stats = player.batting.all().exclude(team='OVR').order_by('-year')
	pitching_stats = player.pitching.all().order_by('-year')

	career_batting_stats = batting_stats.aggregate(
		games=Sum('games'),
		at_bats=Sum('at_bats'),
		runs=Sum('runs'),
		hits=Sum('hits'),
		doubles=Sum('doubles'),
		triples=Sum('triples'),
		home_runs=Sum('home_runs'),
		bases_on_balls=Sum('bases_on_balls'),
		strikeouts=Sum('strikeouts')
	)

	context = {
		'player': player,
		'batting_stats': batting_stats,
		"pitching_stats": pitching_stats,
		'career_batting_stats': career_batting_stats
	}

	modal = render_to_string('modals/playerModal.html', context)
	return JsonResponse({'html': modal})

