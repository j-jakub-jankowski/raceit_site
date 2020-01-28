from django.shortcuts import render
from django_tables2 import RequestConfig

from .models import Competitor, Race, results_data
from .tables import CompetitorTable, ResultsTable, points_column


def index(request):
    return render(request, 'timing/index.html', {})


def race(request):
    """show list od races with short info"""
    race_list = Race.objects.all().order_by('-date_and_time')
    return render(request, 'timing/race.html', {'race_list': race_list})


# '...._active': 'active' - set active status on navbar


def race_info(request, race_id):
    """show information for selected race"""
    race_info_data = Race.objects.get(id=race_id)
    return render(request, 'timing/race_info.html', {'race_info_data': race_info_data,
                                                     'race_info_active': 'active',
                                                     'race_id': race_id})


def start_list(request, race_id):
    """show list of competitors for a given race"""
    table = CompetitorTable(Competitor.objects.filter(race_id=race_id))
    # enable sorting
    RequestConfig(request).configure(table)
    return render(request, 'timing/start_list.html', {'table': table,
                                                      'start_list_active': 'active',
                                                      'race_id': race_id})


def results(request, race_id):
    """show all results for a given race"""
    # create table with extra columns for route points results
    table = ResultsTable(results_data(race_id), extra_columns=points_column(race_id))
    # enable sorting
    RequestConfig(request).configure(table)
    return render(request, 'timing/results.html', {'table': table,
                                                   'results_active': 'active',
                                                   'race_id': race_id})


def live_display(request, race_id):
    """show results as soon as competitor pass timing line"""
    return render(request, 'timing/live_display.html', {'live_display_active': 'active',
                                                        'race_id': race_id})
