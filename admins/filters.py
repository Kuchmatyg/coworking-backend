import django_filters
from users.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains', label='Email contains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Name contains')

    class Meta:
        model = CustomUser
        fields = ['email', 'name']
