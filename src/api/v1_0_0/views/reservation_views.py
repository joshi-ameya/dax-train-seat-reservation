"""Reservation module views."""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status as status_codes

from reservation.models import Reservation
from ..serializers import ReserveSerializer, ReservationDetailsSerializer


class ReservationViewSet(ViewSet):
    """Reservation viewset."""

    @action(methods=["post"], detail=False)
    def reserve(self, request):
        """API to reserve ticket"""

        reserve_serializer = ReserveSerializer(data=request.data)
        if reserve_serializer.is_valid():
            status = status_codes.HTTP_200_OK
            reservation = reserve_serializer.save()
            response = {"message": "successful.", "reservation_number": reservation.reservation_number}
        else:
            status = status_codes.HTTP_400_BAD_REQUEST
            response = reserve_serializer.errors
        return Response(status=status, data=response)

    @action(methods=["get"], detail=False, url_path="details/(?P<reservation_number>[^/.]+)")
    def details(self, request, *args, **kwargs):
        reservation_number = kwargs.get("reservation_number")
        try:
            reservation = Reservation.objects.get(reservation_number=reservation_number)
            status = status_codes.HTTP_200_OK
            reservation_serializer = ReservationDetailsSerializer(reservation)
            data = reservation_serializer.data
        except Reservation.DoesNotExist:
            status = status_codes.HTTP_400_BAD_REQUEST
            data = {"message": "No reservation found."}
        return Response(status=status, data=data)








