from django.urls import path
from .views import (redirect_url,
                    HomeView, 
                    ShortUrlView, 
                    ShortUrlCreate, 
                    ShortUrlUpdate, 
                    ShortUrlDelete, 
                    LandingPageCreate, 
                    LandingPageUpdate, 
                    LandingPageDelete,
                    link_list,
                    link_stats_view,
                    user_click_list,
                    user_clicks)

from django.conf import settings
from django.conf.urls.static import static

app_name = 'tds'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('link-list/', link_list, name='link-list'),
    path('user-click-list/', user_click_list, name='user-click-list'),
    path('user-clicks/<ip>/', user_clicks, name='user-clicks'),
    path('link-stats/<parameter>/', link_stats_view, name='link-stats'),
    path(r'<pk>/view/', ShortUrlView.as_view(), name='short-url-view'),
    path('create-short-url/', ShortUrlCreate.as_view(), name='short-url-create'),
    path(r'<pk>/delete-short-url/', ShortUrlDelete.as_view(), name='short-url-delete'),
    path(r'<pk>/update-short-url/', ShortUrlUpdate.as_view(), name='short-url-update'),

    path(r'<id>/create-landing-page/', LandingPageCreate.as_view(), name='landing-page-create'),
    path(r'<id>/update-landing-page/<pk>/', LandingPageUpdate.as_view(), name='landing-page-update'),
    path(r'<id>/delete-landing-page/<pk>/', LandingPageDelete.as_view(), name='landing-page-delete'),

    path(r'<parameter>/', redirect_url, name='short-url'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
