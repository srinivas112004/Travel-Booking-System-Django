from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelOption, Booking
from .forms import BookingForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth import logout

def index(request):
    recent = TravelOption.objects.order_by('-departure_datetime')[:6]
    return render(request, 'travel/index.html', {'recent': recent})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("travel:index")

def travel_list(request):
    qs = TravelOption.objects.all().order_by('departure_datetime')
    ttype = request.GET.get('type')
    src = request.GET.get('source')
    dst = request.GET.get('destination')
    date = request.GET.get('date')
    q = request.GET.get('q')

    if ttype:
        qs = qs.filter(type__iexact=ttype)
    if src:
        qs = qs.filter(source__icontains=src)
    if dst:
        qs = qs.filter(destination__icontains=dst)
    if date:
        qs = qs.filter(departure_datetime__date=date)
    if q:
        qs = qs.filter(
            Q(source__icontains=q) |
            Q(destination__icontains=q) |
            Q(travel_id__icontains=q)
        )

    paginator = Paginator(qs, 9)
    page = request.GET.get('page')
    travels = paginator.get_page(page)
    return render(request, 'travel/travel_list.html', {'travels': travels, 'q': q})

def travel_detail(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    return render(request, 'travel/travel_detail.html', {'travel': travel})

@login_required
@transaction.atomic
def book_travel(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            travel_locked = TravelOption.objects.select_for_update().get(pk=travel.pk)
            if seats > travel_locked.available_seats:
                form.add_error('number_of_seats', f'Only {travel_locked.available_seats} seats left.')
            else:
                total = seats * travel_locked.price
                booking = Booking.objects.create(
                    user=request.user,
                    travel_option=travel_locked,
                    number_of_seats=seats,
                    total_price=total,
                )
                travel_locked.available_seats -= seats
                travel_locked.save()
                messages.success(request, f'Booking confirmed! ID: {booking.booking_id}')
                return redirect('travel:my_bookings')
    else:
        form = BookingForm(travel_option=travel)
    return render(request, 'travel/booking_form.html', {'form': form, 'travel': travel})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'travel/bookings_list.html', {'bookings': bookings})

@login_required
@transaction.atomic
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'CANCELLED':
        messages.info(request, 'Booking already cancelled.')
        return redirect('travel:my_bookings')
    travel = TravelOption.objects.select_for_update().get(pk=booking.travel_option.pk)
    travel.available_seats += booking.number_of_seats
    travel.save()
    booking.status = 'CANCELLED'
    booking.save()
    messages.success(request, 'Booking cancelled and seats restored.')
    return redirect('travel:my_bookings')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('travel:index')
    else:
        form = UserRegisterForm()
    return render(request, 'travel/register.html', {'form': form})
