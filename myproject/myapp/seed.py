# from django.forms import models
from django.contrib.auth.models import User
from faker import Faker
import random
from .models import Post, Category



# fake = Faker('ru_RU')
fake = Faker()

from datetime import datetime

def run():
    # Создаём категории (если их ещё нет)
    category_names = ['Фэйки', 'Фэйки 2']
    categories = []
    for name in category_names:
        cat, created = Category.objects.get_or_create(name=name)
        categories.append(cat)


    # Создаём несколько случайных продуктов
    for _ in range(10):
        cat = random.choice(categories)
        Post.objects.create(
            title=fake.word().capitalize(),
            body=fake.sentence(nb_words=25),
            # author=user,  # Обязательно указываем реального пользователя
            category=cat,
            created_at=datetime.now(),
            image=None
        )

    print("Данные успешно созданы!")


# from faker import Faker
# import random
# from .models import Post, Category
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from datetime import datetime
#
# fake = Faker('ru_RU')
# User = get_user_model()  # Получаем действующую модель пользователя
#
# def run():
#     # Создаём категории (если их ещё нет)
#     category_names = ['Фэйки', 'Фэйки 2']
#     categories = []
#     for name in category_names:
#         cat, created = Category.objects.get_or_create(name=name)
#         categories.append(cat)
#
#     # Проверяем наличие пользователей и создаём пользователя, если его нет
#     if not User.objects.exists():  # Проверяем наличие хотя бы одного пользователя
#         hashed_password = make_password("testpass")  # Хэшируем пароль перед сохранением
#         user = User.objects.create_user(username="testuser", email="test@example.com", password=hashed_password)
#     else:
#         user = User.objects.first()  # Получаем первого пользователя
#
#     # Создаём несколько случайных постов
#     for _ in range(10):
#         cat = random.choice(categories)
#         Post.objects.create(
#             title=fake.word().capitalize(),
#             body=fake.sentence(nb_words=25),
#             author=user,  # Ставим пользователя автором
#             category=cat,
#             created_at=datetime.now(),
#             image=None
#         )
#
#     print("Данные успешно созданы!")