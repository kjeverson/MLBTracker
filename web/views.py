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

	batting_stats = player.batting.all().exclude(team='TOT').order_by('-year')
	pitching_stats = player.pitching.all().exclude(team='TOT').order_by('-year')

	context = {
		'player': player,
		'batting_stats': batting_stats,
		"pitching_stats": pitching_stats,
		'career_batting_stats': player.batting.filter(team='TOT').first(),
		'career_pitching_stats': player.pitching.filter(team='TOT').first(),
		'current_pitching_stats': pitching_stats.first(),
		'current_batting_stats': batting_stats.first()
	}

	modal = render_to_string('modals/playerModal.html', context)
	return JsonResponse({'html': modal})

