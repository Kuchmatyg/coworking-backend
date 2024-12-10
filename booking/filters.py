import django_filters
from .models import Booking


class BookingFilter(django_filters.FilterSet):
    day = django_filters.DateFilter(field_name="", lookup_expr='date', required=False)

    class Meta:
        model = Booking
        fields = ['day']