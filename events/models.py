from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Registration(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant', 'event')

    def __str__(self):
        return f"{self.participant.name} - {self.event.name}"