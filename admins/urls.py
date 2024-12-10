from django.urls import path
from admins.views import GetAllUsersView, CreateGroupView, GetUsersByGroupView, FilterUsersView

urlpatterns = [
    path('users/', GetAllUsersView.as_view(), name='get_all_users'),
    #path('user/<str:email>/', GetUserByEmailView.as_view(), name='get_user_by_email'),
    path('group/create/', CreateGroupView.as_view(), name='create_group'),
    path('users/group/<uuid:group_id>/', GetUsersByGroupView.as_view(), name='get_users_by_group'),
    path('users/filter/', FilterUsersView.as_view(), name='filter_users'),  # Новый маршрут для фильтрации
]