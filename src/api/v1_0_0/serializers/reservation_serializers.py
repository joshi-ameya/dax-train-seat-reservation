"""Reservation module serializers."""

import secrets
import string

from django.db.models import Sum, Q
from rest_framework import serializers

from reservation.constants import CABIN_TYPE_CHOICES
from reservation.models import Train, Cabin, TrainCabin, Reservation


class ReserveSerializer(serializers.Serializer):
    """Serializer for reserve ticket."""

    train = serializers.CharField(max_length=28)
    cabin = serializers.ChoiceField(choices=CABIN_TYPE_CHOICES)
    no_of_seats = serializers.IntegerField()
    date = serializers.DateField()

    def validate_train(self, value):
        """Validate train no."""

        try:
            train = Train.objects.get(train_no=value)
        except Train.DoesNotExist:
            raise serializers.ValidationError("No train found")
        return train

    def validate_cabin(self, value):
        """Validate train no."""

        cabins = Cabin.objects.filter(type=value)
        if not cabins:
            raise serializers.ValidationError("Invalid cabin selected")
        return cabins


    def validate(self, validated_data):
        """Method to validate reservation information."""
        train = validated_data.get("train")
        cabins = validated_data.get("cabin")
        no_of_seats = validated_data.get("no_of_seats")
        date = validated_data.pop("date")
        validated_data.update({
            "date_of_travel": date
        })
        errors = {}
        try:
            # If train travels on given day of week.
            weekday = date.strftime('%A')[:3].lower()
            if weekday not in validated_data.get("train").travel_days:
                errors.update({
                    "date": [
                        f"Train is not available on {weekday} of week"
                    ]
                })
                raise serializers.ValidationError(errors)
            # If this cabin is available to this train.
            train_cabins = TrainCabin.objects.filter(train=train, cabin__in=cabins)
            if train_cabins:
                # Now get all reservation made for combination of (Train X Cabin X Date of travel).
                results = Reservation.objects.filter(
                    train=train, cabin__in=cabins, date_of_travel=date
                ).values("cabin__type").annotate(reserved_seats=Sum("no_of_seats"))
                if not results:
                    # This means no reservation for this Train X Cabin is made till now,
                    # so we will make reservation in first cabin
                    validated_data.update({
                        "date_of_travel": date,
                        "reservation_number": ReserveSerializer.generate_reservation_number(),
                        "cabin": cabins[0]
                    })
                    return validated_data

                # There are some reservation made, so we will check which cart has seats available.
                reservations = {res.get("cabin__type"): res.get("reserved_seats") for res in results}
                cabin_found = False
                for train_cabin in train_cabins:
                    if reservations.get(train_cabin.cabin.type) <= train_cabin.no_of_seats:
                        available_seats = train_cabin.no_of_seats - reservations.get(train_cabin.cabin.type)
                        if available_seats >= no_of_seats:
                            # Available in this Cart.
                            validated_data.update({
                                "cabin": train_cabin.cabin
                            })
                            cabin_found = True
                            break

                if not cabin_found:
                    # No. of seats are not available for asked cabin type, so we will generate suggestions.
                    suggestions = ReserveSerializer.get_available_seats_in_train(validated_data=validated_data)
                    if suggestions:
                        errors.update({
                            "suggestions": suggestions,
                            "message": "There are not enough seats in mentioned cabins, you can select anyone of the available cabins, if interested"
                        })
                    else:
                        errors.update({
                            "message": "Sorry, train does not have enough seats available."
                        })
            else:
                errors.update({
                    "cabin": ["This cabin is not available to this train."]
                })
        except serializers.ValidationError:
            pass
        except Exception as e:
            errors.update({
                "error": str(e)
            })
        if errors:
            raise serializers.ValidationError(errors)
        validated_data.update({
            "date_of_travel": date,
            "reservation_number": ReserveSerializer.generate_reservation_number()
        })
        return validated_data

    @staticmethod
    def get_available_seats_in_train(validated_data):
        """Method to get available seats in other cabins."""
        all_other_cabins = TrainCabin.objects.exclude(
            cabin__in=validated_data.get("cabin")).values_list("cabin__type").annotate(Sum("cabin__no_of_seats"))
        results = Reservation.objects.filter(
            Q(train=validated_data.get("train")),
            Q(date_of_travel=validated_data.get("date_of_travel")),
            ~Q(cabin__in=validated_data.get("cabin"))
        ).values("cabin__type").annotate(reserved_seats=Sum("no_of_seats"))
        all_other_cabins = {res[0]: res[1] for res in all_other_cabins}
        reserved_seats_per_cabin_type = {res["cabin__type"]: res["reserved_seats"] for res in results}
        available_cabins = []
        for cabin_type, seats in all_other_cabins.items():
            if not(cabin_type in reserved_seats_per_cabin_type) or (cabin_type in reserved_seats_per_cabin_type and seats >= reserved_seats_per_cabin_type[cabin_type]):
                available_seats = seats - reserved_seats_per_cabin_type.get(cabin_type, 0)
                if available_seats >= validated_data.get("no_of_seats"):
                    available_cabins.append({
                        "cabin_type": cabin_type,
                        "available_seats": available_seats
                    })
        return available_cabins

    @staticmethod
    def generate_reservation_number():
        """Method to generate a reservation number."""

        length = 10
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)


class TrainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ('train_no', "destination", "source", "start_time", "end_time")


class CabinModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ("type", "name", "description")


class ReservationDetailsSerializer(serializers.ModelSerializer):
    train = TrainModelSerializer()
    cabin = CabinModelSerializer()
    date_of_reservation = serializers.DateTimeField(read_only=True, source="created_at")

    class Meta:
        model = Reservation
        fields = ("train", "cabin", "reservation_number", "no_of_seats", "date_of_travel", "date_of_reservation")
