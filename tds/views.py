from django.shortcuts import render, redirect, get_object_or_404

from utils.helpers import get_users_ip_address, fill_user_click_stats, fill_user_click_stats_red_to_default
from utils.helpers import generate_graph
from .models import ShortenUrl, RedirectLink, UserClickStat
from django.contrib.gis.geoip2 import GeoIP2
from django.urls import reverse_lazy
from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

import random


class HomeView(LoginRequiredMixin, ListView):
    context_object_name = 'short_url'
    template_name = "home.html"

    def get_queryset(self):
        return ShortenUrl.objects.filter(user=self.request.user)


class ShortUrlView(LoginRequiredMixin, DetailView):
    model = ShortenUrl
    template_name = "short_url_detail.html"


class ShortUrlCreate(LoginRequiredMixin, CreateView):
    model = ShortenUrl
    fields = ['user', 'parameter', 'link']
    template_name = "short_url_form.html"

    def get_initial(self):
        import string
        s = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
        return {
            'user': self.request.user,
            'parameter': str(s)
        }


class ShortUrlUpdate(LoginRequiredMixin, UpdateView):
    model = ShortenUrl
    fields = ['parameter', 'link']
    template_name = "short_url_form.html"

    def get_object(self):
        return ShortenUrl.objects.get(user=self.request.user, pk=self.kwargs['pk'])


class ShortUrlDelete(LoginRequiredMixin, DeleteView):
    model = ShortenUrl
    success_url = reverse_lazy('tds:home')


class LandingPageCreate(LoginRequiredMixin, CreateView):
    model = RedirectLink
    fields = ['parameter', 'url', 'country', 'weight']
    template_name = "landing_url_form.html"

    def get_initial(self):
        return {
            'parameter': get_object_or_404(ShortenUrl, pk=self.kwargs['id']),
            'weight': 0,
        }


class LandingPageUpdate(LoginRequiredMixin, UpdateView):
    model = RedirectLink
    fields = ['parameter', 'url', 'country', 'weight']
    template_name = "landing_url_form.html"

    def get_object(self):
        return RedirectLink.objects.get(parameter__user=self.request.user, pk=self.kwargs['pk'])


class LandingPageDelete(LoginRequiredMixin, DeleteView):
    model = RedirectLink

    def get_success_url(self):
        return reverse_lazy('tds:short-url-view', kwargs={'pk': self.object.parameter_id})


def redirect_url(request, parameter):
    try:
        shorten_url = ShortenUrl.objects.get(
            parameter=parameter
            )

        users_ip_address = get_users_ip_address(request)

        g = GeoIP2()
        location = g.city(users_ip_address)
        location_code = location["country_code"]

        by_country_qs = RedirectLink.objects.filter(
            parameter=shorten_url,
            country=location_code
        ).order_by('-weight')

        by_weight_qs = RedirectLink.objects.filter(
            parameter=shorten_url,
            country=None
        ).order_by('-weight')

        if by_country_qs.exists():
            url = by_country_qs[0]
            same_weight_lp = RedirectLink.objects.filter(
                parameter=shorten_url,
                country=location_code,
                weight=url.weight
            )

            url = random.choice(same_weight_lp)
            fill_user_click_stats(users_ip_address, shorten_url, parameter, url)

            return redirect(url.url)
        
        elif by_weight_qs.exists():
            url = by_weight_qs[0]
            same_weight_lp = RedirectLink.objects.filter(
                parameter=shorten_url,
                country=None,
                weight=url.weight
            )

            url = random.choice(same_weight_lp)
            fill_user_click_stats(users_ip_address, shorten_url, parameter, url)

            return redirect(url.url)

        fill_user_click_stats_red_to_default(users_ip_address, shorten_url, parameter)
        return redirect(shorten_url.link)

    except ObjectDoesNotExist:
        return redirect("/")


def user_click_list(request):

    if request.user.is_anonymous:
        return redirect('accounts/login/')

    user_ip = UserClickStat.objects.filter(
        url_created_by=request.user
    ).values('ip').distinct()

    context = {
        "user_ip": user_ip,
    }

    return render(request, "user_click_list.html", context)


@login_required
def user_clicks(request, ip):
    user_ip = UserClickStat.objects.filter(
                                    ip=ip,
                                    url_created_by=request.user
    ).order_by('-time')
    
    context = {
        "user_ip": user_ip,
    }

    return render(request, "user_clicks.html", context)


@login_required
def link_stats_view(request, parameter):
    user_click = UserClickStat.objects.filter(
        parameter=parameter,
        url_created_by=request.user
    ).order_by('-time')

    user_click_distinct = UserClickStat.objects.filter(
        parameter=parameter,
        url_created_by=request.user
    ).values('ip').distinct()

    total_click = user_click.count()
    unique_click = user_click_distinct.count()

    data_click = []
    data_updated = []
    objects_a = []

    for i in range(24):
        hr = i + 1
        time_threshold = timezone.now() - timedelta(hours=hr)
        user_click_24 = UserClickStat.objects.filter(
            parameter=parameter, time__gte=time_threshold,
            url_created_by=request.user
        )

        data_click.append(user_click_24.count())

    hr24 = data_click[23]

    for i in range(24):
        data_updated.append(0)
        data_click[i] = 0
        data_click[i] = UserClickStat.objects.filter(
            parameter=parameter, time__hour__gte=i, time__hour__lt=i + 1,
            url_created_by=request.user
        ).count()

    short = ShortenUrl.objects.get(
        parameter=parameter
    )

    hr_now = timezone.now().hour

    for i in range(24 - hr_now):
        data_updated[i] = data_click[hr_now + i]
        objects_a.append(hr_now + i)

    for i in range(hr_now):
        data_updated[24 - hr_now + i] = data_click[i]
        objects_a.append(i)

    generate_graph(data_updated, objects_a)

    context = {
        "short": short,
        "total_click": total_click,
        "unique_click": unique_click,
        "data_click": data_click,
        "hr24": hr24,
        "user_click": user_click_24
    }

    return render(request, "link_stats.html", context)


def link_list(request):

    if request.user.is_anonymous:
        return redirect('accounts/login/')

    short_url = ShortenUrl.objects.filter(
        user=request.user
    )

    context = {
        "short_url": short_url,
    }

    return render(request, "link_list.html", context)
