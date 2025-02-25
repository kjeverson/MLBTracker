from django.urls import path
from .views import PlayerListCreate, BattingStatsByYearView, PitchingStatsByYearView

urlpatterns = [
    path('players/', PlayerListCreate.as_view(), name='item-list'),
    path('batting-stats/<int:year>/', BattingStatsByYearView.as_view(),
         name='batting-stats-by-year'),
    path('pitching-stats/<int:year>/', PitchingStatsByYearView.as_view(),
         name='pitching-stats-by-year')
]
