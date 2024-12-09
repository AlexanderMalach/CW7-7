from rest_framework import serializers

from habits.serializers import HabitSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    habits = HabitSerializer(source="users_habits", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
