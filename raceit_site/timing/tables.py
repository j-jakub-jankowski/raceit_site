import itertools

import django_tables2 as tables
from django_tables2 import Column, A

from .models import Competitor, RoutePoint


class CompetitorTable(tables.Table):
    """table of competitors for a given race"""
    class Meta:
        model = Competitor
        exclude = ('id', 'race',)
        template_name = "django_tables2/bootstrap4.html"


def points_column(race_id):
    """get list of route points for a given race"""
    column = []
    for p in list(RoutePoint.objects.filter(race_id=race_id).values_list('point_name', flat=True)):
        column.append((p, Column()))
    return column


class ResultsTable(tables.Table):
    """table with results"""
    place = tables.Column(empty_values=(), orderable=False)
    bib = tables.Column()
    name = tables.Column()
    surname = tables.Column()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_place(self):
        row = next(self.counter)
        row = row + 1
        return f'{row}'

    class Meta:
        template_name = "django_tables2/bootstrap.html"
