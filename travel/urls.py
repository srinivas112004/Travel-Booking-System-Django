from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'travel'

urlpatterns = [
    path('', views.index, name='index'),
    path('travel/', views.travel_list, name='list'),
    path('travel/<int:pk>/', views.travel_detail, name='detail'),
    path('travel/<int:pk>/book/', views.book_travel, name='book'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='travel/login.html'), name='login'),
    # custom GET logout
    path('logout/', views.logout_view, name='logout'),
]
