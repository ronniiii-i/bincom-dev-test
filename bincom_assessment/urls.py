from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.polling_unit_result, name='polling_unit_result'),
    path('lga-summary/', views.lga_summed_result, name='lga_summed_result'),
    path('add-polling-unit/', views.add_polling_unit, name='add_polling_unit'),
    path('api/wards/<int:lga_id>/', views.get_wards, name='get_wards'),
]