from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

# Этот декоратор подписывает функцию на сигнал post_save модели Product
@receiver(post_save, sender=Post)
def post_created_signal(sender, instance, created, **kwargs):
    if created:
        # Если объект только что создан
        print(f"Создано: {instance.title}")
    else:
        # Если объект обновлён
        print(f"Обновлёно: {instance.title}")