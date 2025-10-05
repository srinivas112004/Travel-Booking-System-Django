from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Q, Avg, F
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Booking, TravelOption
from decimal import Decimal


def superuser_required(function):
    """Decorator to ensure only superusers can access admin views"""
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/login/'
    )
    return actual_decorator(function)


@superuser_required
def admin_dashboard(request):
    """Main admin dashboard with statistics and charts"""
    
    # Time periods
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # === BOOKING STATISTICS ===
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='CONFIRMED').count()
    cancelled_bookings = Booking.objects.filter(status='CANCELLED').count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    
    # Today's bookings
    todays_bookings = Booking.objects.filter(booking_date__date=today).count()
    
    # This week's bookings
    week_bookings = Booking.objects.filter(booking_date__gte=week_ago).count()
    
    # This month's bookings
    month_bookings = Booking.objects.filter(booking_date__gte=month_ago).count()
    
    # === REVENUE STATISTICS ===
    total_revenue = Booking.objects.filter(status='CONFIRMED').aggregate(
        total=Sum('total_price')
    )['total'] or Decimal('0')
    
    week_revenue = Booking.objects.filter(
        status='CONFIRMED', 
        booking_date__gte=week_ago
    ).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
    
    month_revenue = Booking.objects.filter(
        status='CONFIRMED',
        booking_date__gte=month_ago
    ).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
    
    # Total refunds issued
    total_refunds = Booking.objects.filter(
        status='CANCELLED',
        refund_amount__isnull=False
    ).aggregate(total=Sum('refund_amount'))['total'] or Decimal('0')
    
    # === USER STATISTICS ===
    total_users = User.objects.count()
    active_users = User.objects.filter(
        booking__booking_date__gte=month_ago
    ).distinct().count()
    
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    new_users_month = User.objects.filter(date_joined__gte=month_ago).count()
    
    # === TRAVEL STATISTICS ===
    total_travel_options = TravelOption.objects.count()
    
    # Bookings by travel type
    bookings_by_type = Booking.objects.filter(status='CONFIRMED').values(
        'travel_option__type'
    ).annotate(count=Count('id')).order_by('-count')
    
    # Popular routes
    popular_routes = Booking.objects.filter(status='CONFIRMED').values(
        'travel_option__source',
        'travel_option__destination'
    ).annotate(count=Count('id')).order_by('-count')[:10]
    
    # === RECENT ACTIVITY ===
    recent_bookings = Booking.objects.select_related(
        'user', 'travel_option'
    ).order_by('-booking_date')[:10]
    
    recent_cancellations = Booking.objects.filter(
        status='CANCELLED'
    ).select_related('user', 'travel_option').order_by('-cancelled_at')[:5]
    
    # === TOP USERS ===
    top_users = User.objects.annotate(
        booking_count=Count('booking', filter=Q(booking__status='CONFIRMED')),
        total_spent=Sum('booking__total_price', filter=Q(booking__status='CONFIRMED'))
    ).filter(booking_count__gt=0).order_by('-total_spent')[:10]
    
    # === AVAILABILITY STATISTICS ===
    low_availability = TravelOption.objects.filter(
        available_seats__lte=5,
        departure_datetime__gte=timezone.now()
    ).order_by('available_seats')[:10]
    
    # === CHART DATA ===
    # Bookings trend (last 7 days)
    bookings_trend = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Booking.objects.filter(booking_date__date=date).count()
        bookings_trend.append({
            'date': date.strftime('%b %d'),
            'count': count
        })
    
    # Revenue trend (last 7 days)
    revenue_trend = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        revenue = Booking.objects.filter(
            status='CONFIRMED',
            booking_date__date=date
        ).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
        revenue_trend.append({
            'date': date.strftime('%b %d'),
            'revenue': float(revenue)
        })
    
    context = {
        # Booking stats
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'pending_bookings': pending_bookings,
        'todays_bookings': todays_bookings,
        'week_bookings': week_bookings,
        'month_bookings': month_bookings,
        
        # Revenue stats
        'total_revenue': total_revenue,
        'week_revenue': week_revenue,
        'month_revenue': month_revenue,
        'total_refunds': total_refunds,
        
        # User stats
        'total_users': total_users,
        'active_users': active_users,
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        
        # Travel stats
        'total_travel_options': total_travel_options,
        'bookings_by_type': bookings_by_type,
        'popular_routes': popular_routes,
        
        # Recent activity
        'recent_bookings': recent_bookings,
        'recent_cancellations': recent_cancellations,
        
        # Top users
        'top_users': top_users,
        
        # Availability
        'low_availability': low_availability,
        
        # Chart data
        'bookings_trend': bookings_trend,
        'revenue_trend': revenue_trend,
    }
    
    return render(request, 'travel/admin/dashboard.html', context)


@superuser_required
def admin_bookings(request):
    """Admin view for managing all bookings"""
    bookings = Booking.objects.select_related('user', 'travel_option').order_by('-booking_date')
    
    # Filters
    status_filter = request.GET.get('status')
    user_search = request.GET.get('user')
    travel_type = request.GET.get('travel_type')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if user_search:
        bookings = bookings.filter(
            Q(user__username__icontains=user_search) |
            Q(user__email__icontains=user_search) |
            Q(user__first_name__icontains=user_search) |
            Q(user__last_name__icontains=user_search)
        )
    if travel_type:
        bookings = bookings.filter(travel_option__type=travel_type)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'user_search': user_search,
        'travel_type': travel_type,
    }
    return render(request, 'travel/admin/bookings.html', context)


@superuser_required
def admin_users(request):
    """Admin view for managing users"""
    users = User.objects.annotate(
        booking_count=Count('booking'),
        total_spent=Sum('booking__total_price', filter=Q(booking__status='CONFIRMED'))
    ).order_by('-date_joined')
    
    # Search
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    context = {
        'users': users,
        'search': search,
    }
    return render(request, 'travel/admin/users.html', context)


@superuser_required
def admin_travel_options(request):
    """Admin view for managing travel options"""
    travel_options = TravelOption.objects.annotate(
        booking_count=Count('booking'),
        revenue=Sum('booking__total_price', filter=Q(booking__status='CONFIRMED'))
    ).order_by('-departure_datetime')
    
    # Filters
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    
    if travel_type:
        travel_options = travel_options.filter(type=travel_type)
    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if destination:
        travel_options = travel_options.filter(destination__icontains=destination)
    
    context = {
        'travel_options': travel_options,
        'travel_type': travel_type,
        'source': source,
        'destination': destination,
    }
    return render(request, 'travel/admin/travel_options.html', context)
