from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/', views.race, name='race'),
    path('race/<int:race_id>/', views.race_info, name='race_info'),
    path('race/<int:race_id>/start_list/', views.start_list, name='start_list'),
    path('race/<int:race_id>/results/', views.results, name='results'),
    path('race/<int:race_id>/live_display/', views.live_display, name='live_display'),
]
