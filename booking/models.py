from django.db import models
import uuid
from users.models import CustomUser


class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    

    def __str__(self):
        return self.name
    

# Модель Booking (Бронирование)
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Уникальный ID брони
    classroom = models.ForeignKey(Classroom, related_name='bookings', on_delete=models.CASCADE)  # Связь с Classroom
    user = models.ForeignKey(CustomUser, related_name='bookings', on_delete=models.CASCADE)  # Связь с User (пользователь)
    from_time = models.PositiveIntegerField()  # Время начала брони
    to_time = models.PositiveIntegerField()  # Время окончания брони
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания брони
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время последнего обновления

    # def __str__(self):
    #     return f"Booking for {self.classroom.name} by {self.user.username} from {self.from_time} to {self.to_time}"

    # class Meta:
    #     # Уникальное ограничение: нельзя создать бронирование, если время пересекается с другим бронированием
    #     constraints = [
    #         models.UniqueConstraint(fields=['classroom', 'from_time', 'to_time'], name='unique_booking_time')
    #     ]
