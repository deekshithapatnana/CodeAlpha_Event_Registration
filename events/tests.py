from django.test import TestCase
from django.urls import reverse
from .models import Event, Participant, Registration


class EventRegistrationTests(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name="Test Tech Fest",
            description="Test technology event",
            date="2026-09-01T10:00:00Z",
            location="Test Auditorium",
            capacity=2
        )

    def test_event_list(self):
        response = self.client.get("/events/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Tech Fest")

    def test_create_event(self):
        response = self.client.post(
            "/events/",
            data={
                "name": "New Tech Event",
                "description": "A new technology event",
                "date": "2026-09-10T10:00:00Z",
                "location": "College Hall",
                "capacity": 100
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 2)

    def test_successful_registration(self):
        response = self.client.post(
            "/register/",
            data={
                "name": "Test Student",
                "email": "teststudent@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Registration.objects.count(), 1)

    def test_duplicate_registration(self):
        self.client.post(
            "/register/",
            data={
                "name": "Test Student",
                "email": "teststudent@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        response = self.client.post(
            "/register/",
            data={
                "name": "Test Student",
                "email": "teststudent@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Participant already registered"
        )

    def test_event_capacity(self):
        self.client.post(
            "/register/",
            data={
                "name": "Student One",
                "email": "student1@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        self.client.post(
            "/register/",
            data={
                "name": "Student Two",
                "email": "student2@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        response = self.client.post(
            "/register/",
            data={
                "name": "Student Three",
                "email": "student3@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Event is full"
        )

    def test_invalid_event(self):
        response = self.client.post(
            "/register/",
            data={
                "name": "Test Student",
                "email": "student@example.com",
                "event_id": 999
            },
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"],
            "Event not found"
        )

    def test_registration_list(self):
        self.client.post(
            "/register/",
            data={
                "name": "Test Student",
                "email": "student@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        response = self.client.get("/registrations/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Student")

    def test_cancel_registration(self):
        response = self.client.post(
            "/register/",
            data={
                "name": "Cancel Student",
                "email": "cancel@example.com",
                "event_id": self.event.id
            },
            content_type="application/json"
        )

        registration_id = response.json()["registration_id"]

        cancel_response = self.client.delete(
            f"/registrations/{registration_id}/cancel/"
        )

        self.assertEqual(cancel_response.status_code, 200)
        self.assertEqual(Registration.objects.count(), 0)


from django.test import TestCase

# Create your tests here.
