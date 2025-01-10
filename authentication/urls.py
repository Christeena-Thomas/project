from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


from . import views
from .views import change_password
from .views import servicce
from .views import about
from.views import register_views
from.views import duphome


urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('register_views/',views.register_views,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('nav/',views.nav_view,name='nav'),
  
    path('excel-files/', views.excel_file_list, name='excel_file_list'),
    path('excel-files/<int:file_id>/', views.excel_file_view, name='excel_file_view'),
    # Add more URLs as needed

    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('change-password/', change_password, name='change_password'),
    path('service/', servicce, name='servicce'),
    path('aboutt/', about, name='about'),
    path('duphome/', duphome, name='duphome'),
    path('displayxl/',views.displayxl,name='displayxl'),
    path('events/',views.events_and_trainings, name='events'),
    path('prediction/',views.prediction, name='prediction'),
    path('notifications/',views.notifications, name='notifications'),
]

