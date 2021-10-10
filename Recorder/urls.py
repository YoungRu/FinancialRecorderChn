from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('total/', views.total, name='total'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('redelete/<int:pk>', views.Redelete, name='Redelete'),
    path('exdelete/<int:pk>', views.Exdelete, name='Exdelete'),
    path('ladelete/<int:pk>', views.Ladelete, name='Ladelete'),
    path('pdf/', views.pdf, name='pdf'),
    path('crsl/', views.crsl, name='crsl'),
    path('history/', views.history, name='history'),
    path('record_csv/', views.record_csv, name='record_csv'),
    path('period_record_csv/', views.period_record_csv, name='period_record_csv'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)