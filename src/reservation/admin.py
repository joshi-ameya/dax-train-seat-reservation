"""Reservation module admin forms."""

from django.contrib import admin
from reservation.models import Train, Cabin, TrainCabin, Reservation


class TrainAdmin(admin.ModelAdmin):
    pass


class CabinAdmin(admin.ModelAdmin):
    pass


class TrainCabinAdmin(admin.ModelAdmin):
    pass


class ReservationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Train, TrainAdmin)
admin.site.register(Cabin, CabinAdmin)
admin.site.register(TrainCabin, TrainCabinAdmin)
admin.site.register(Reservation, ReservationAdmin)
