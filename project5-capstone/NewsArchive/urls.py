from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),#homepage
    path('dashboard',views.dashboard_view,name="dashboard_view"),
    path("login", views.login_view,name="login"),
    path("logout", views.logout_view,name="logout"),
    path("register", views.register_view,name="register"),
    path("config_save",views.config_save,name="config_view"),
    path("aggregate_info",views.aggregate_info,name="aggregate_info_view"),# todays aggregation information
    path("month_info/<str:date>",views.month_info,name="month_info_view"),  # months aggregation information
    path("day_data/<str:date>",views.day_data,name="day_data_view"),
    path("month_data/<str:date>",views.month_data,name="month_data_view"),
]
