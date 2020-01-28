import queue
import threading

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist

from .models import Result, Competitor

channel_layer = get_channel_layer()
read_queue = queue.Queue()
threads = {}


def start_reading_files(queryset):
    """create threads to read data from Chronotrack file """
    # to read chrono file
    for file in queryset:
        thread = threading.Thread(target=read_chrono_file, args=(file,), daemon=True)
        threads[file.id] = thread
        threads[file.id].start()

    queryset.update(reading_flag='True')


def stop_reading_files(queryset):
    for file in queryset:
        pass
    queryset.update(reading_flag='False')
    pass


def read_chrono_file(file):
    """open file, read k line from path and put result into queue"""
    k = 0
    file_path = file.chrono_file_path
    file_point = file.point
    while True:
        with open(file_path, 'r', -1, 'utf-8') as file:
            try:
                last_line = file.readlines()[k]
                last_line = last_line.split(',')
                read_queue.put([file_point, last_line[2], last_line[3], last_line[4]])
                k += 1
            except IndexError:
                pass


def save_read():
    """get result from queue and save in database"""
    while True:
        point, chrono, tag, time = read_queue.get()
        try:
            c = Competitor.objects.get(tag_id=tag)
            new_result = Result(competitor=c, tag=tag, point=point, gun_time=time)
            async_to_sync(channel_layer.group_send)('chat',
                                                    {'type': 'send_result', 'bib': c.tag.bib_number, 'name': c.name,
                                                     'surname': c.surname, 'point': point.point_name, 'time': time
                                                     })
        except ObjectDoesNotExist:
            new_result = Result(tag=tag, point=point, gun_time=time)
        new_result.save()


save_result_thread = threading.Thread(target=save_read, daemon=True)
save_result_thread.start()
