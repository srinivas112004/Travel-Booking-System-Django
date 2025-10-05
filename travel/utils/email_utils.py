"""
Utility functions for sending emails in the travel booking system
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email to the user
    """
    subject = f'Booking Confirmation - {booking.booking_id}'
    
    # Context for email template
    context = {
        'booking': booking,
        'user': booking.user,
        'travel': booking.travel_option,
    }
    
    # Render HTML email
    html_content = render_to_string('travel/emails/booking_confirmation.html', context)
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending booking confirmation email: {e}")
        return False


def send_cancellation_email(booking):
    """
    Send booking cancellation email to the user
    """
    subject = f'Booking Cancelled - {booking.booking_id}'
    
    # Calculate cancellation fee
    cancellation_fee = booking.total_price - (booking.refund_amount if booking.refund_amount else 0)
    
    context = {
        'booking': booking,
        'user': booking.user,
        'travel': booking.travel_option,
        'refund_amount': booking.refund_amount,
        'cancellation_fee': cancellation_fee,
        'site_url': 'http://127.0.0.1:8000',  # Update for production
    }
    
    html_content = render_to_string('travel/emails/booking_cancellation.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending cancellation email: {e}")
        return False


def send_reminder_email(booking):
    """
    Send booking reminder email 24 hours before departure
    """
    subject = f'Travel Reminder - Departure Tomorrow'
    
    context = {
        'booking': booking,
        'user': booking.user,
        'travel': booking.travel_option,
    }
    
    html_content = render_to_string('travel/emails/booking_reminder.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending reminder email: {e}")
        return False
