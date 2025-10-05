from django.urls import path
from . import views
from .profile_views import user_profile, edit_profile, change_password, booking_history
from .admin_views import admin_dashboard, admin_bookings, admin_users, admin_travel_options
from django.contrib.auth import views as auth_views

app_name = 'travel'

urlpatterns = [
    path('', views.index, name='index'),
    path('travel/', views.travel_list, name='list'),
    path('travel/<int:pk>/', views.travel_detail, name='detail'),
    path('travel/<int:pk>/book/', views.book_travel, name='book'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:pk>/download-ticket/', views.download_ticket, name='download_ticket'),
    path('booking/<int:pk>/download-receipt/', views.download_cancellation_receipt, name='download_receipt'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='travel/login.html'), name='login'),
    # custom GET logout
    path('logout/', views.logout_view, name='logout'),
    
    # User Profile URLs
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('profile/booking-history/', booking_history, name='booking_history'),
    
    # Admin Dashboard URLs (using 'dashboard/' to avoid conflict with Django admin)
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/bookings/', admin_bookings, name='admin_bookings'),
    path('dashboard/users/', admin_users, name='admin_users'),
    path('dashboard/travel-options/', admin_travel_options, name='admin_travel_options'),
]
