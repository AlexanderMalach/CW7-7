from datetime import timedelta
from celery import shared_task
from django.db import transaction
from django.utils.timezone import now

from habits.models import Habit
from habits.services import send_telegram_message
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

@shared_task
def send_message_to_user():
    """
    Отправляет уведомления пользователям о выполнении их привычек, прибавляя 2 дня после отправки.
    """
    current_date = now().date()
    habits = Habit.objects.filter(sign_of_a_pleasant_habit=False)

    for habit in habits:
        try:
            with transaction.atomic():
                # Если `next_reminder_date` не установлена, инициализируем её
                if not habit.next_reminder_date:
                    habit.next_reminder_date = current_date
                    habit.save(update_fields=["next_reminder_date"])
                    continue

                # Проверяем, пришло ли время для отправки напоминания
                if current_date >= habit.next_reminder_date:
                    # Формируем и отправляем сообщение
                    if habit.owner.tg_chat_id:
                        message = (
                            f"Напоминание: сегодня выполнение привычки '{habit.habit}'! "
                            f"Место: {habit.place_of_execution or 'не указано'}, время: {habit.time_execution or 'в любое время'}."
                        )
                        send_telegram_message(message=message, chat_id=habit.owner.tg_chat_id)
                    else:
                        logger.warning(f"Пропущено: у пользователя {habit.owner.id} нет Telegram ID.")

                    # Обновляем дату следующего напоминания
                    habit.next_reminder_date += timedelta(days=habit.periodicity)
                    habit.save(update_fields=["next_reminder_date"])

        except Exception as e:
            logger.error(f"Ошибка обработки привычки ID {habit.id}: {e}")
