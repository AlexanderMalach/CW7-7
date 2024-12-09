from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка модели Habit
    """
    list_display = (
        "id",
        "habit",
        "sign_of_a_pleasant_habit",
        "related_habit",
        "reward",
    )
    list_filter = ("sign_of_a_pleasant_habit",)
    search_fields = ("habit",)
    ordering = ("id",)
