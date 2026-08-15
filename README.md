# Event Registration System

A Django-based backend API for managing events and participant registrations.

## Features

- Create and view events
- Register participants for events
- Prevent duplicate registrations
- Check event capacity
- View all registrations
- Cancel registrations
- JSON-based API responses
- SQLite database
- Django admin support
- Input validation
- Automated tests

## Technologies Used

- Python
- Django
- SQLite
- REST-style JSON APIs
- Django Test Framework

## Project Structure

```text
CodeAlpha_Event_Registration/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── events/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
└── README.md