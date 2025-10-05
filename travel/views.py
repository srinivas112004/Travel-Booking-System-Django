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
from django.http import HttpResponse
from django.utils import timezone
from .utils.email_utils import send_booking_confirmation_email, send_cancellation_email
from .utils.pdf_utils import generate_ticket_pdf, generate_cancellation_receipt_pdf

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
    
    # Check if seats are available
    if travel.available_seats <= 0:
        messages.error(request, 'Sorry, this travel option is sold out.')
        return redirect('travel:detail', pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            travel_locked = TravelOption.objects.select_for_update().get(pk=travel.pk)
            
            # Double-check availability with locked record
            if seats > travel_locked.available_seats:
                form.add_error('number_of_seats', f'Only {travel_locked.available_seats} seats left.')
            else:
                try:
                    total = seats * travel_locked.price
                    booking = Booking.objects.create(
                        user=request.user,
                        travel_option=travel_locked,
                        number_of_seats=seats,
                        total_price=total,
                    )
                    travel_locked.available_seats -= seats
                    travel_locked.save()
                    
                    # Send confirmation email
                    try:
                        send_booking_confirmation_email(booking)
                    except Exception as email_error:
                        # Don't fail the booking if email fails
                        print(f"Email notification failed: {email_error}")
                    
                    messages.success(request, f'Booking confirmed! ID: {booking.booking_id}. Check your email for confirmation.')
                    return redirect('travel:my_bookings')
                except Exception as e:
                    messages.error(request, f'Booking failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
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
    
    # Check if booking can be cancelled
    if not booking.can_cancel():
        messages.error(request, 'Booking cannot be cancelled. Cancellations must be made at least 2 hours before departure.')
        return redirect('travel:my_bookings')
    
    # Calculate refund
    refund_amount = booking.calculate_refund()
    cancellation_fee = booking.total_price - refund_amount
    
    # Calculate cancellation percentage
    if refund_amount == 0:
        cancellation_percentage = 100
    else:
        cancellation_percentage = int((cancellation_fee / booking.total_price) * 100)
    
    # If GET request, show cancellation confirmation page
    if request.method == 'GET':
        context = {
            'booking': booking,
            'refund_amount': refund_amount,
            'cancellation_fee': cancellation_fee,
            'cancellation_percentage': cancellation_percentage,
        }
        return render(request, 'travel/cancel_booking.html', context)
    
    # If POST request, process the cancellation
    elif request.method == 'POST':
        travel = TravelOption.objects.select_for_update().get(pk=booking.travel_option.pk)
        travel.available_seats += booking.number_of_seats
        travel.save()
        
        booking.status = 'CANCELLED'
        booking.cancelled_at = timezone.now()
        booking.refund_amount = refund_amount
        # Get cancellation reason from POST or GET, default to standard message
        booking.cancellation_reason = request.POST.get('reason') or 'User requested cancellation'
        booking.save()
        
        # Send cancellation email
        try:
            send_cancellation_email(booking)
        except Exception as email_error:
            print(f"Cancellation email failed: {email_error}")
        
        if refund_amount > 0:
            messages.success(request, f'Booking cancelled successfully! Refund of ${refund_amount:.2f} will be processed within 5-7 business days.')
        else:
            messages.warning(request, 'Booking cancelled. No refund available as per cancellation policy.')
        
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

@login_required
def download_ticket(request, pk):
    """Download PDF ticket for a confirmed booking"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if booking.status != 'CONFIRMED':
        messages.error(request, 'Ticket is only available for confirmed bookings.')
        return redirect('travel:my_bookings')
    
    try:
        pdf = generate_ticket_pdf(booking)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{booking.booking_id}.pdf"'
        return response
    except Exception as e:
        messages.error(request, f'Failed to generate ticket: {str(e)}')
        return redirect('travel:my_bookings')

@login_required
def download_cancellation_receipt(request, pk):
    """Download PDF receipt for a cancelled booking"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if booking.status != 'CANCELLED':
        messages.error(request, 'Receipt is only available for cancelled bookings.')
        return redirect('travel:my_bookings')
    
    try:
        pdf = generate_cancellation_receipt_pdf(booking)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="cancellation_receipt_{booking.booking_id}.pdf"'
        return response
    except Exception as e:
        messages.error(request, f'Failed to generate receipt: {str(e)}')
        return redirect('travel:my_bookings')
