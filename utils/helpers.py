import datetime

from tds.models import UserClickStat
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')


def get_users_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def fill_user_click_stats(users_ip, shorten_url, parameter, url):
    user = UserClickStat()
    user.ip = users_ip
    user.url_created_by = shorten_url.user
    user.parameter = parameter
    user.url = url.url
    user.save()


def fill_user_click_stats_red_to_default(users_ip, shorten_url, parameter):
    user = UserClickStat()
    user.ip = users_ip
    user.url_created_by = shorten_url.user
    user.parameter = parameter
    user.url = shorten_url.link
    user.save()


def generate_graph(data_updated, objects_a):
    hours = [datetime.time(i).strftime('%H') for i in range(24)]
    objects_display = [hours[objects_a[i]] for i in range(24)]

    data_latest = data_updated[0]

    for i in range(24 - 1):
        data_updated[i] = data_updated[i + 1]

    data_updated[23] = data_latest

    object_latest = objects_display[0]

    for i in range(24 - 1):
        objects_display[i] = objects_display[i + 1]

    objects_display[23] = object_latest

    plt.clf()
    y_pos = np.arange(len(objects_display))
    plt.bar(y_pos, data_updated, align='center', alpha=0.5, width=0.8)
    plt.xticks(y_pos, objects_display)
    plt.xlabel('Hours')
    plt.ylabel('Clicks')
    plt.title('Clicks distribution in last 24 hours')
    plt.savefig('media/graph.png')

