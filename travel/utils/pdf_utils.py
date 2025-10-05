"""
Utility functions for generating PDF tickets
"""
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from django.conf import settings
import qrcode
import os


def generate_ticket_pdf(booking):
    """
    Generate a PDF ticket for the booking
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=6
    )
    
    # Title
    title = Paragraph("E-TICKET", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Booking Status Badge
    status_color = colors.HexColor('#28a745') if booking.status == 'CONFIRMED' else colors.HexColor('#dc3545')
    status_data = [[Paragraph(f"<b>Status: {booking.status}</b>", 
                              ParagraphStyle('status', parent=normal_style, 
                                           textColor=colors.white, alignment=TA_CENTER))]]
    status_table = Table(status_data, colWidths=[2*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), status_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
    ]))
    elements.append(status_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Booking Information
    elements.append(Paragraph("Booking Information", heading_style))
    
    booking_data = [
        ['Booking ID:', str(booking.booking_id)],
        ['Booking Date:', booking.booking_date.strftime('%B %d, %Y %I:%M %p')],
        ['Passenger Name:', booking.user.get_full_name() or booking.user.username],
        ['Email:', booking.user.email],
    ]
    
    booking_table = Table(booking_data, colWidths=[2*inch, 4*inch])
    booking_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ]))
    elements.append(booking_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Travel Details
    elements.append(Paragraph("Travel Details", heading_style))
    
    travel = booking.travel_option
    travel_data = [
        ['Travel ID:', travel.travel_id],
        ['Type:', f"{travel.type} {'✈️' if travel.type == 'FLIGHT' else '🚂' if travel.type == 'TRAIN' else '🚌'}"],
        ['Route:', f"{travel.source} → {travel.destination}"],
        ['Departure:', travel.departure_datetime.strftime('%B %d, %Y at %I:%M %p')],
        ['Number of Seats:', str(booking.number_of_seats)],
    ]
    
    travel_table = Table(travel_data, colWidths=[2*inch, 4*inch])
    travel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ]))
    elements.append(travel_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Summary
    elements.append(Paragraph("Payment Summary", heading_style))
    
    payment_data = [
        ['Price per Seat:', f"${travel.price}"],
        ['Number of Seats:', str(booking.number_of_seats)],
        ['Total Amount:', f"${booking.total_price}"],
    ]
    
    payment_table = Table(payment_data, colWidths=[2*inch, 4*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 2), (1, 2), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (0, 1), colors.HexColor('#495057')),
        ('TEXTCOLOR', (0, 2), (1, 2), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTSIZE', (0, 2), (1, 2), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Generate QR Code
    qr_data = f"BOOKING:{booking.booking_id}|USER:{booking.user.email}|TRAVEL:{travel.travel_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code temporarily
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # Add QR Code to PDF
    elements.append(Paragraph("Scan QR Code for Verification", heading_style))
    qr_image = Image(qr_buffer, width=1.5*inch, height=1.5*inch)
    elements.append(qr_image)
    elements.append(Spacer(1, 0.2*inch))
    
    # Important Notes
    elements.append(Spacer(1, 0.2*inch))
    notes_style = ParagraphStyle(
        'Notes',
        parent=normal_style,
        fontSize=9,
        textColor=colors.HexColor('#6c757d'),
        leftIndent=20
    )
    
    elements.append(Paragraph("<b>Important Information:</b>", heading_style))
    elements.append(Paragraph("• Please arrive at the departure point at least 30 minutes before departure time.", notes_style))
    elements.append(Paragraph("• Carry a valid photo ID for verification.", notes_style))
    elements.append(Paragraph("• This ticket is non-transferable.", notes_style))
    elements.append(Paragraph("• Cancellation policy: Refunds available up to 2 hours before departure.", notes_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=normal_style,
        fontSize=9,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Thank you for choosing TravelBooking!", footer_style))
    elements.append(Paragraph("For support, contact us at support@travelbooking.com", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def generate_cancellation_receipt_pdf(booking):
    """
    Generate a PDF receipt for cancelled booking
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#dc3545'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=6
    )
    
    # Title
    title = Paragraph("CANCELLATION RECEIPT", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Cancellation Info
    elements.append(Paragraph("Cancellation Information", heading_style))
    
    cancel_data = [
        ['Booking ID:', str(booking.booking_id)],
        ['Original Booking Date:', booking.booking_date.strftime('%B %d, %Y %I:%M %p')],
        ['Cancellation Date:', booking.cancelled_at.strftime('%B %d, %Y %I:%M %p') if booking.cancelled_at else 'N/A'],
        ['Passenger:', booking.user.get_full_name() or booking.user.username],
        ['Travel Route:', f"{booking.travel_option.source} → {booking.travel_option.destination}"],
        ['Original Amount:', f"${booking.total_price}"],
        ['Refund Amount:', f"${booking.refund_amount if booking.refund_amount else 0}"],
        ['Cancellation Fee:', f"${booking.total_price - (booking.refund_amount if booking.refund_amount else 0)}"],
    ]
    
    cancel_table = Table(cancel_data, colWidths=[2.5*inch, 3.5*inch])
    cancel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 6), (1, 6), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (0, 5), colors.HexColor('#495057')),
        ('TEXTCOLOR', (0, 6), (1, 6), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ]))
    elements.append(cancel_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Refund Note
    note_style = ParagraphStyle(
        'Note',
        parent=normal_style,
        fontSize=10,
        textColor=colors.HexColor('#856404'),
        backColor=colors.HexColor('#fff3cd'),
        borderPadding=10,
        leftIndent=10,
        rightIndent=10
    )
    elements.append(Paragraph("<b>Refund Processing:</b> The refund amount will be credited to your original payment method within 5-7 business days.", note_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
