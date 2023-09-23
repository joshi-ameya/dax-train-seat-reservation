"""Models file for reservation module."""

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django import forms

from reservation.constants import WEEKDAYS_CHOICES, CABIN_TYPE_CHOICES
from utils.models import BaseCustomModel


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class Train(BaseCustomModel,):
    """Train model class."""

    train_no = models.CharField(max_length=5, db_index=True) # e.g. 12228, 12227
    name = models.CharField(max_length=256) # Name like Duronto express, Vande Bharat, etc.
    destination = models.CharField(max_length=28)  # Largest cityname in India is 28
    source = models.CharField(max_length=28)  # Largest cityname in India is 28
    start_time = models.TimeField()
    end_time = models.TimeField()
    travel_days = ChoiceArrayField(
            models.CharField(max_length=10, blank=True, choices=WEEKDAYS_CHOICES),
            default=list
    )

    def __str__(self):
        return f"{self.train_no}"


class Cabin(BaseCustomModel,):
    """Cabin Model class."""

    type = models.CharField(max_length=20, choices=CABIN_TYPE_CHOICES)
    name = models.CharField(max_length=10)  # A1, A2, A3
    description = models.TextField()
    no_of_seats = models.SmallIntegerField()

    def __str__(self):
        return f"{self.name} - {self.type}"


class TrainCabin(BaseCustomModel,):
    """Train-Cabin count model class."""

    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    no_of_seats = models.SmallIntegerField()


class Reservation(BaseCustomModel,):
    """Reservation model class."""

    reservation_number = models.CharField(max_length=10, db_index=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    no_of_seats = models.SmallIntegerField()
    date_of_travel = models.DateField()
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)








