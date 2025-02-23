from django.urls import path, include
from web.views import home, get_player_modal

urlpatterns = [
	path('', home, name='home'),
	path('api/', include('api.urls')),
	path('get-player-modal/<int:player_id>/', get_player_modal, name='get_player_modal'),
]

