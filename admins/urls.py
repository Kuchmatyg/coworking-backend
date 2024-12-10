from django.urls import path
from admins.views import GetAllUsersView, CreateGroupView, GetUsersByGroupView, FilterUsersView, GetAll, \
    CreateClassroomView, UpdateGroupView, UpdateClassroomView, UpdateBookingView, DeleteGroupView, DeleteClassroomView, \
    DeleteBookingView

urlpatterns = [
    path('users', GetAllUsersView.as_view(), name='get_all_users'),
    #path('user/<str:email>/', GetUserByEmailView.as_view(), name='get_user_by_email'),
    path('users/groups/<uuid:group_id>', GetUsersByGroupView.as_view(), name='get_users_by_group'),
    path('users/filter', FilterUsersView.as_view(), name='filter_users'),
    path('get_all', GetAll.as_view(), name='get_all'),

    path('groups/create', CreateGroupView.as_view(), name='create-group'),
    path('classrooms/create', CreateClassroomView.as_view(), name='create-classroom'),

    path('groups/update/<uuid:id>', UpdateGroupView.as_view(), name='update-group'), # +
    path('classrooms/update/<uuid:id>', UpdateClassroomView.as_view(), name='update-classroom'),
    path('bookings/update/<uuid:id>', UpdateBookingView.as_view(), name='update-booking'),

    path('groups/delete/<uuid:id>', DeleteGroupView.as_view(), name='delete-group'),
    path('classrooms/delete/<uuid:id>', DeleteClassroomView.as_view(), name='delete-classroom'),
    path('bookings/delete/<uuid:id>', DeleteBookingView.as_view(), name='delete-booking'),
]