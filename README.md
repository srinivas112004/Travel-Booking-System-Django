# 🚀 Travel Booking System

A modern, feature-rich travel booking platform built with Django 5.2.5. Book flights, trains, and buses with an intuitive interface, email notifications, PDF tickets, and comprehensive admin dashboard.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.2.5-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🎫 **Booking Management**
- **Multi-Type Travel**: Book flights, trains, and buses
- **Real-time Availability**: Live seat availability tracking
- **Smart Search**: Filter by type, source, destination, and date
- **Booking Confirmation**: Instant booking with unique booking IDs
- **Cancellation System**: Cancel bookings with refund calculation
  - Flight: 80% refund
  - Train: 70% refund
  - Bus: 60% refund
- **Booking History**: Complete history with status filters

### 📧 **Email Notifications**
- **Booking Confirmation**: HTML email with booking details
- **Cancellation Confirmation**: Email with refund breakdown
- **24-Hour Reminders**: Automatic reminder before departure
- **Professional Templates**: Beautiful, responsive email designs

### 📄 **PDF Generation**
- **E-Tickets**: Download tickets with QR codes for verification
- **Cancellation Receipts**: PDF receipt with refund details
- **Booking Summary**: Complete payment and journey information
- **QR Code Integration**: Scannable codes for quick verification

### 👤 **User Profile Management**
- **Personal Dashboard**: View statistics and recent bookings
- **Profile Editing**: Update personal information and preferences
- **Password Management**: Secure password change functionality
- **Booking History**: Detailed history with advanced filters
- **Statistics**: Total bookings, amount spent, loyalty tracking

### 📊 **Admin Dashboard** (Superuser Only)
- **Analytics Dashboard**: 
  - Total bookings, revenue, users, cancellations
  - 7-day booking and revenue trends
  - Popular routes analysis
  - Recent activity monitoring
- **Booking Management**: View and filter all bookings
- **User Management**: Search and manage all users
- **Travel Options**: Monitor and manage inventory
- **Real-time Statistics**: Live data updates

### 🎨 **Modern UI/UX**
- **Glassmorphism Design**: Frosted glass effects and backdrop blur
- **Gradient Themes**: Beautiful purple and green gradients
- **Smooth Animations**: 
  - Float, pulse, shimmer, slide-in effects
  - Hover lift animations
  - Ripple button effects
  - Rotating backgrounds
- **Enhanced Forms**: 
  - Password strength meter
  - Show/hide password toggle
  - Live validation feedback
  - Icon-enhanced inputs
- **Responsive Design**: Mobile-first, works on all devices
- **Interactive Elements**: Animated navigation, dropdowns, badges

### 🔐 **Authentication & Security**
- **User Registration**: With password strength validation
- **Secure Login**: Session-based authentication
- **Enhanced Forms**: Modern, animated login/register pages
- **Role-based Access**: Superuser-only admin dashboard
- **CSRF Protection**: Built-in security features

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.5
- **Language**: Python 3.10.0
- **Database**: SQLite (default) / MySQL (configurable)
- **ORM**: Django ORM

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)
- **Animations**: Custom CSS animations

### Libraries & Tools
- **PDF Generation**: ReportLab 4.0.0+
- **QR Codes**: qrcode 7.4.2+
- **Image Processing**: Pillow 10.0.0+
- **Email**: Django Email Framework

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd travel_booking_System
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📋 Usage Guide

### For Regular Users:

1. **Register Account**
   - Navigate to `/register/`
   - Fill in personal details
   - Password strength meter guides secure password creation

2. **Search & Book Travel**
   - Browse available options on homepage
   - Filter by type, source, destination, date
   - Select seats and confirm booking
   - Download PDF e-ticket

3. **Manage Bookings**
   - View all bookings in "My Bookings"
   - Download tickets anytime
   - Cancel bookings (refund calculated automatically)

4. **Profile Management**
   - Click username → "My Profile"
   - Update personal information
   - View booking statistics
   - Check complete booking history
   - Change password

### For Administrators (Superuser):

1. **Access Admin Dashboard**
   - Login with superuser account
   - Click "Admin Dashboard" in navigation

2. **Monitor System**
   - View real-time statistics
   - Analyze booking trends
   - Track revenue and cancellations
   - Identify popular routes

3. **Manage Resources**
   - View all bookings with filters
   - Search and manage users
   - Monitor travel options inventory
   - Check seat availability

4. **Django Admin Panel**
   - Access: `/admin/`
   - Full database management
   - Create/edit travel options
   - Manage users and permissions

---

## 🗂️ Project Structure

```
travel_booking_System/
│
├── travel/                          # Main application
│   ├── migrations/                  # Database migrations
│   ├── static/travel/              
│   │   └── css/
│   │       └── styles.css          # Enhanced modern UI styles
│   ├── templates/travel/
│   │   ├── admin/                  # Admin dashboard templates
│   │   │   ├── dashboard.html
│   │   │   ├── bookings.html
│   │   │   ├── users.html
│   │   │   └── travel_options.html
│   │   ├── emails/                 # Email templates
│   │   │   ├── booking_confirmation.html
│   │   │   ├── cancellation_email.html
│   │   │   └── reminder_email.html
│   │   ├── profile/                # Profile templates
│   │   │   ├── profile.html
│   │   │   ├── edit_profile.html
│   │   │   ├── change_password.html
│   │   │   └── booking_history.html
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Homepage
│   │   ├── login.html              # Enhanced login
│   │   ├── register.html           # Enhanced register
│   │   ├── travel_list.html
│   │   ├── travel_detail.html
│   │   ├── booking_form.html
│   │   ├── bookings_list.html
│   │   └── cancel_booking.html
│   ├── utils/
│   │   ├── email_utils.py          # Email sending functions
│   │   └── pdf_utils.py            # PDF generation utilities
│   ├── models.py                   # Database models
│   ├── views.py                    # Main views
│   ├── profile_views.py            # Profile management views
│   ├── admin_views.py              # Admin dashboard views
│   ├── forms.py                    # Booking forms
│   ├── profile_forms.py            # Profile forms
│   ├── urls.py                     # URL routing
│   └── admin.py                    # Django admin config
│
├── travel_booking/                 # Project settings
│   ├── settings.py                 # Configuration
│   ├── urls.py                     # Root URL config
│   └── wsgi.py
│
├── db.sqlite3                      # Database (SQLite)
├── manage.py                       # Django management
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## ⚙️ Configuration

### Email Settings

**Development Mode** (Default - Console):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails print to terminal/console.

**Production Mode** (Real Emails):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Database Options

**SQLite** (Default):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**MySQL** (Optional):
Set environment variable `USE_MYSQL=1` and configure:
```python
MYSQL_DATABASE = 'travel_db'
MYSQL_USER = 'travel_user'
MYSQL_PASSWORD = 'password'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
```

---

## 📊 Database Models

### **TravelOption**
- `travel_id`: Unique identifier
- `type`: Flight/Train/Bus
- `source`, `destination`: Route details
- `departure_datetime`, `arrival_datetime`
- `price`: Per seat price
- `available_seats`: Real-time availability
- `total_seats`: Total capacity

### **Booking**
- `booking_id`: UUID unique identifier
- `user`: ForeignKey to User
- `travel_option`: ForeignKey to TravelOption
- `seats_booked`: Number of seats
- `total_price`: Calculated price
- `status`: CONFIRMED/CANCELLED
- `booking_date`: Timestamp
- `cancelled_at`: Cancellation timestamp
- `cancellation_reason`: User input
- `refund_amount`: Calculated refund

### **UserProfile**
- `user`: OneToOne with User
- `phone_number`: Contact number
- `date_of_birth`: DOB
- `gender`: Male/Female/Other
- `address`: Full address fields
- `travel_preferences`: User preferences
- `bio`: User bio
- `newsletter_subscription`: Boolean

---

## 🎯 Key Features Explained

### Refund Calculation
```python
def calculate_refund(self):
    if self.status != 'CANCELLED':
        return Decimal('0.00')
    
    refund_percentages = {
        'FLIGHT': Decimal('0.80'),  # 80%
        'TRAIN': Decimal('0.70'),   # 70%
        'BUS': Decimal('0.60'),     # 60%
    }
    
    percentage = refund_percentages.get(
        self.travel_option.type, 
        Decimal('0.50')
    )
    
    return (self.total_price * percentage).quantize(
        Decimal('0.01'), 
        rounding=ROUND_HALF_UP
    )
```

### Email Notifications
- **Booking Confirmation**: Sent immediately after booking
- **Cancellation Email**: Sent when booking is cancelled
- **Reminder Email**: Sent 24 hours before departure (can be triggered manually)

### PDF Ticket Features
- Unique QR code for verification
- Booking ID and travel details
- Passenger information
- Payment summary
- Travel route and timings

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Configure real email backend (SMTP)
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up HTTPS/SSL
- [ ] Configure media files storage
- [ ] Set up backup strategy
- [ ] Enable logging
- [ ] Configure CORS if needed

---

## 📸 Screenshots

### Homepage
Modern search interface with gradient backgrounds and glassmorphism effects.

### Booking Management
View all bookings with download and cancel options.

### Admin Dashboard
Comprehensive analytics with charts, trends, and statistics.

### User Profile
Personal dashboard with booking history and statistics.

### Login/Register
Enhanced forms with animations and password strength meter.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Srinivas Kandagatla**
- Email: srinivas.kandagatla112004@gmail.com

---

## 🙏 Acknowledgments

- Django Framework
- Bootstrap CSS
- Font Awesome Icons
- ReportLab for PDF generation
- All open-source contributors

---

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: srinivas.kandagatla112004@gmail.com

---

## 🗓️ Version History

### v2.0.0 (Current)
- ✨ Enhanced UI with modern animations
- 📧 Email notification system
- 📄 PDF ticket generation with QR codes
- 👤 User profile management
- 📊 Admin dashboard with analytics
- 🎨 Glassmorphism design
- 🔐 Enhanced authentication forms
- 💳 Refund calculation system

### v1.0.0
- 🎫 Basic booking system
- 🔍 Search and filter
- 👥 User authentication
- 📱 Responsive design

---

**Made with ❤️ using Django**
