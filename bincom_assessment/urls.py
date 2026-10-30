from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.polling_unit_result, name='polling_unit_result'),
    path('lga-summary/', views.lga_summed_result, name='lga_summed_result'),
]