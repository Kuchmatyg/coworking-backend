
from django.urls import path
from booking.views import BookingListView, BookingCreateView, GetClassroomBookingsView, UserBookingsView, ClassroomsView

urlpatterns = [
    path('', BookingListView.as_view(), name="booking"),
    path('create', BookingCreateView.as_view(), name='create_booking'),
    path('booked', GetClassroomBookingsView.as_view(), name='get_classroom_bookings'),
    path('my', UserBookingsView.as_view(), name='user_bookings'),
    path('classrooms', ClassroomsView.as_view(), name='classrooms'),
]