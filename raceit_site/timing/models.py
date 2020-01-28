from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone


class Race(models.Model):
    """instance of race with basic info"""
    name = models.CharField(max_length=100)
    distance = models.FloatField()
    date_and_time = models.DateTimeField(blank=True, null=True)
    town = models.CharField(max_length=100)
    race_info = RichTextField(blank=True)
    race_rules = RichTextField(blank=True)
    race_route = RichTextField(blank=True)

    def __str__(self):
        date = self.date_and_time.strftime('%d-%m-%Y')
        return f'{date} {self.name}'


class RoutePoint(models.Model):
    """points on route with time measurement"""
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    point_name = models.CharField(max_length=10)
    point_distance = models.FloatField()

    def __str__(self):
        return f'{self.race} {self.point_name}'


class ChronoFile(models.Model):
    """path to Chronotrack files with reads
    Normal - most accurate - official results - processing by device - 5s
    Immediate - accuracy on the level of 1-2s - live display - available immediately"""
    Normal = 1
    Immediate = 2
    TYPES = (
        (1, 'Normal'),
        (2, 'Immediate'),
    )
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE)
    file_type = models.PositiveSmallIntegerField(choices=TYPES, default=Normal)
    chrono_file_path = models.FilePathField(
        path='/home/jakub/PythonProjects/RaceIT_project/RaceIT/raceit_site/chrono_files/')
    reading_flag = models.BooleanField()

    def __str__(self):
        path = self.chrono_file_path
        t = self.file_type
        return f'{t} {path}'


class Tag(models.Model):
    """pairs of tag (RFID tag ID) and bib numbers permanently assigned before race"""
    tag = models.CharField(max_length=5, primary_key=True, unique=True)
    bib_number = models.CharField(max_length=10)

    def __str__(self):
        return self.bib_number


class Competitor(models.Model):
    """competitor info
    tag related with RFID chip are unique"""
    tag = models.OneToOneField(Tag, on_delete=models.SET(0))
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    team = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        competitor_info = f'{self.tag.bib_number} {self.name} {self.surname}'
        return competitor_info


class Result(models.Model):
    """competitor result on route points"""
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='results',
                                   related_query_name='results', null=True, blank=True)
    tag = models.CharField(max_length=5)
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE)
    gun_time = models.CharField(max_length=11)

    def __str__(self):
        result_info = f'{self.point} {self.tag} {self.gun_time}'
        return result_info


def results_data(race_id):
    """join competitors with them results for a particular race
    |bib_number|name|surname|result1|result2|...."""
    data = []
    competitors = Competitor.objects.filter(race_id=race_id).prefetch_related('results')
    for c in competitors:
        # create dictionary with competitor info
        c_info = {'bib': c.tag.bib_number, 'name': c.name, 'surname': c.surname}
        # get all results for a given competitor
        c_results = c.results.all()
        for points in c_results:
            # add dictionary item with result for route point (point: gun_time) to competitor
            c_info[points.point.point_name] = points.gun_time
        # add data to list of competitors
        data.append(c_info)
    return data


class ChronoResult(models.Model):
    """raw data from Chronotrack devices, manually added times with proper flags"""
    tag = models.CharField(max_length=50)
    chrono = models.CharField(max_length=50)
    gun_time = models.CharField(max_length=11)

    def add_result(self):
        self.result = timezone.now()
        self.save()