import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Participant, Registration


@csrf_exempt
def event_list(request):

    # GET - List all events
    if request.method == 'GET':
        events = Event.objects.all()

        data = []

        for event in events:
            data.append({
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "date": event.date,
                "location": event.location,
                "capacity": event.capacity
            })

        return JsonResponse(data, safe=False)

    # POST - Create a new event
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )

        required_fields = [
            'name',
            'description',
            'date',
            'location',
            'capacity'
        ]

        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {"error": f"Missing required field: {field}"},
                    status=400
                )

        if not isinstance(data['capacity'], int) or data['capacity'] <= 0:
            return JsonResponse(
                {"error": "Capacity must be a positive integer"},
                status=400
            )

        event = Event.objects.create(
            name=data['name'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            capacity=data['capacity']
        )

        return JsonResponse({
            "message": "Event created successfully",
            "event_id": event.id,
            "event": event.name
        }, status=201)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


@csrf_exempt
def register_participant(request):

    # Only POST is allowed
    if request.method != 'POST':
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    # Read JSON data
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    # Check required fields
    required_fields = ['name', 'email', 'event_id']

    for field in required_fields:
        if field not in data:
            return JsonResponse(
                {"error": f"Missing required field: {field}"},
                status=400
            )

    name = data['name']
    email = data['email']
    event_id = data['event_id']

    # Check whether event exists
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse(
            {"error": "Event not found"},
            status=404
        )

    # Check event capacity
    current_registrations = Registration.objects.filter(
        event=event
    ).count()

    if current_registrations >= event.capacity:
        return JsonResponse(
            {"error": "Event is full"},
            status=400
        )

    # Create participant if they don't already exist
    participant, created = Participant.objects.get_or_create(
        email=email,
        defaults={"name": name}
    )

    # Prevent duplicate registration
    if Registration.objects.filter(
        participant=participant,
        event=event
    ).exists():
        return JsonResponse(
            {"error": "Participant already registered"},
            status=400
        )

    # Create registration
    registration = Registration.objects.create(
        participant=participant,
        event=event
    )

    return JsonResponse({
        "message": "Registration successful",
        "registration_id": registration.id,
        "participant": participant.name,
        "email": participant.email,
        "event": event.name
    }, status=201)


def registration_list(request):

    # Only GET is allowed
    if request.method != 'GET':
        return JsonResponse(
            {"error": "Only GET requests are allowed"},
            status=405
        )

    registrations = Registration.objects.select_related(
        'participant',
        'event'
    ).all()

    data = []

    for registration in registrations:
        data.append({
            "registration_id": registration.id,
            "participant": registration.participant.name,
            "email": registration.participant.email,
            "event": registration.event.name,
            "registered_at": registration.registered_at
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def cancel_registration(request, registration_id):

    # Only DELETE is allowed
    if request.method != 'DELETE':
        return JsonResponse(
            {"error": "Only DELETE requests are allowed"},
            status=405
        )

    # Find registration
    try:
        registration = Registration.objects.get(
            id=registration_id
        )
    except Registration.DoesNotExist:
        return JsonResponse(
            {"error": "Registration not found"},
            status=404
        )

    # Delete registration
    registration.delete()

    return JsonResponse({
        "message": "Registration cancelled successfully"
    })