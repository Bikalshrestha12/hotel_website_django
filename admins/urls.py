from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    # path('', index, name='indext'),
    path('', admin_dashboard, name='dasboard'),
    # path('', TemplateView.as_view(template_name='adminlte/index.html')),
    # path('', TemplateView.as_view(template_name='adminlte/login.html')),
] 