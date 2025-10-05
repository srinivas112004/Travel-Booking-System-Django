from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile
from .profile_forms import UserProfileForm, ChangePasswordForm
from .models import Booking, TravelOption


@login_required
def user_profile(request):
    """Display user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get user statistics
    total_bookings = Booking.objects.filter(user=request.user).count()
    confirmed_bookings = Booking.objects.filter(user=request.user, status='CONFIRMED').count()
    cancelled_bookings = Booking.objects.filter(user=request.user, status='CANCELLED').count()
    total_spent = Booking.objects.filter(user=request.user, status='CONFIRMED').aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')[:5]
    
    context = {
        'profile': profile,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_spent': total_spent,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'travel/profile/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('travel:user_profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'travel/profile/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Password changed successfully!')
            return redirect('travel:user_profile')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'travel/profile/change_password.html', {'form': form})


@login_required
def booking_history(request):
    """View complete booking history with filters"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Filters
    status_filter = request.GET.get('status')
    travel_type = request.GET.get('travel_type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if travel_type:
        bookings = bookings.filter(travel_option__type=travel_type)
    if date_from:
        bookings = bookings.filter(booking_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(booking_date__lte=date_to)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'travel_type': travel_type,
    }
    return render(request, 'travel/profile/booking_history.html', context)
