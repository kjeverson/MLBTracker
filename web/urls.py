from django.urls import path, include
from web.views import get_player_modal, batting, pitching, players

urlpatterns = [
	path('', players, name='players'),
	path('players/', players, name='players'),
	path('batting/', batting, name='batting'),
	path('pitching/', pitching, name='pitching'),
	path('api/', include('api.urls')),
	path('get-player-modal/<int:player_id>/', get_player_modal, name='get_player_modal'),
]

