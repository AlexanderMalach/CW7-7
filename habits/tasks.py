from datetime import datetime
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
    Отправляет уведомления пользователям о выполнении их привычек с учётом периодичности и времени выполнения.
    """
    current_time = now()
    habits = Habit.objects.filter(sign_of_a_pleasant_habit=False)

    for habit in habits:
        try:
            with transaction.atomic():
                # Рассчитываем прошедшее время с момента последнего обновления
                last_updated = habit.updated_at or habit.created_at
                elapsed_days = (current_time.date() - last_updated.date()).days

                if elapsed_days > 0:
                    # Уменьшаем `send_indicator` с учётом прошедших дней
                    habit.send_indicator -= elapsed_days

                    # Проверяем необходимость отправки уведомления
                    if habit.send_indicator <= 0 and habit.time_execution:
                        # Проверяем соответствие текущего времени времени выполнения привычки
                        execution_time = datetime.combine(current_time.date(), habit.time_execution)
                        if current_time >= execution_time:
                            # Формируем и отправляем сообщение
                            if habit.owner.tg_chat_id:
                                message = (
                                    f"Напоминание: сегодня выполнение привычки '{habit.habit}'! "
                                    f"Место: {habit.place_of_execution or 'не указано'}, время: {habit.time_execution}."
                                )
                                send_telegram_message(message=message, chat_id=habit.owner.tg_chat_id)
                            else:
                                logger.warning(f"Пропущено: у пользователя {habit.owner.id} нет Telegram ID.")

                            # Сбрасываем `send_indicator` на периодичность
                            habit.send_indicator = habit.periodicity

                    # Обновляем время последнего изменения
                    habit.updated_at = current_time

                    # Сохраняем изменения
                    habit.save(update_fields=["send_indicator", "updated_at"])

        except Exception as e:
            # Логируем общую ошибку обработки привычки
            logger.error(f"Ошибка обработки привычки ID {habit.id}: {e}")
