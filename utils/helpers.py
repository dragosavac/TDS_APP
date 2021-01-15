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


def create_user(users_ip, shorten_url, parameter, url):
    user = UserClickStat()
    user.ip = users_ip
    user.url_created_by = shorten_url.user
    user.parameter = parameter
    user.url = url.url
    user.save()


def generate_graph(data_click):
    objects = []

    for i in range(24):
        objects.append(i + 1)

    plt.clf()
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, data_click, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Clicks')
    plt.title('Clicks distribution in last 24 hours')
    plt.savefig('media/graph.png')
