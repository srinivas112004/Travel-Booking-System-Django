✈️ Travel Booking System (Django)

A Django-based Travel Booking System with support for MySQL/SQLite. Users can search, book, and cancel travel options (Flights, Trains, Buses). Includes authentication, validations, and admin management.

🚀 Live Demo: https://srinivas07.pythonanywhere.com

🔑 Features:

• User Registration, Login, Logout

• Browse & search travel options with filters (type, source, destination, date)

• Booking with seat validation (prevents overbooking)

• Cancel bookings → seats auto-restored

• Admin panel to manage Travel Options & Bookings

• Unit tests for booking, cancellation, and filtering

🛠️ Tech Stack:

• Backend: Django 4.x

• Database: MySQL 8 / SQLite3 (switchable)

• Frontend: Bootstrap 5 + Django Templates

• Deployment: PythonAnywhere

⚙️ Setup Project Locally :

1️⃣ Clone repo

git clone https://github.com/yourusername/travel-booking-system-django.git cd travel_booking_system

2️⃣ Create virtual environment

python -m venv venv # Activate venv # Windows: venv\Scripts\activate # Linux/Mac: source venv/bin/activate 

3️⃣ Install dependencies

pip install -r requirements.txt 

4️⃣ Apply migrations

python manage.py makemigrations python manage.py migrate 

5️⃣ Create superuser (for admin access)

python manage.py createsuperuser 

6️⃣ Run the server

python manage.py runserver 

Now open 👉 http://127.0.0.1:8000/

🗄️ MySQL Setup (Optional)

CREATE DATABASE travel_db; CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON travel_db.* TO 'travel_user'@'localhost'; FLUSH PRIVILEGES; 

Then set environment variables or .env:

USE_MYSQL=1 MYSQL_DATABASE=travel_db MYSQL_USER=travel_user MYSQL_PASSWORD=password MYSQL_HOST=localhost MYSQL_PORT=3306 

✅ Unit Tests:

python manage.py test 


👨‍💻 Author:

Developed by Srinivas Kandagatla
Deployment:https://srinivas07.pythonanywhere.com

