# from faker import Faker
# import random
# from .models import Post, Category
#
#
#
# fake = Faker('ru_RU')
#
#
# from datetime import datetime
#
# def run():
#     # Создаём категории (если их ещё нет)
#     category_names = ['Новости', 'Отдых', 'Фэйки', 'Фэйки 2']
#     categories = []
#     for name in category_names:
#         cat, created = Category.objects.get_or_create(name=name)
#         categories.append(cat)
#
#
#     # Создаём несколько случайных продуктов
#     for _ in range(10):
#         cat = random.choice(categories)
#         Post.objects.create(
#             title=fake.word().capitalize(),
#             body=fake.sentence(nb_words=25),
#             # author=user,  # Обязательно указываем реального пользователя
#             category=cat,
#             created_at=datetime.now(),
#             image=None
#         )
#
#     print("Данные успешно созданы!")


from faker import Faker
import random
from myapp.models import ShopProduct, ShopCategory
from django.utils.timezone import now
from django.contrib.auth.models import User  # Импортируем модель пользователя

fake = Faker(['ru_RU'])  # Используем русский язык для генератора фейковых данных

# def run():
#     # Получаем первый существующий аккаунт пользователя
#     user = User.objects.first()
#     if not user:
#         raise Exception("Нет зарегистрированных пользователей. Нужно создать хотя бы одного.")
#
#     # Создаём категории (если их ещё нет)
#     category_names = ['Новости', 'Отдых', 'Фейки']
#     categories = []
#     for name in category_names:
#         cat, created = Category.objects.get_or_create(name=name)
#         categories.append(cat)
#
#     # Создаём несколько случайных записей в блоге
#     for _ in range(100):
#         cat = random.choice(categories)
#         post = Post.objects.create(
#             title=fake.word().capitalize(),
#             body=fake.sentence(nb_words=25),
#             author=user,  # Автор поста
#             category=cat,
#             created_at=now(),  # Время создания поста в UTC
#             image=None
#         )
#
#     print("Данные успешно созданы!")

def run():
    category_names = ['Ноутбуки', 'Смартфоны', 'Аксессуары', 'Гаджеты']
    categories = []
    for name in category_names:
        cat, created = ShopCategory.objects.get_or_create(name_Shop=name)
        categories.append(cat)


    for _ in range(50):
        cat = random.choice(categories)
        ShopProduct.objects.create(
            name_Shop=fake.word().capitalize() + ' ' + cat.name_Shop,
            description_Shop=fake.sentence(nb_words=8),
            price_Shop=round(random.uniform(100, 2000), 2),
            in_stock_Shop=random.choice([True, False]),
            category_Shop=cat
        )

    print("Данные успешно созданы!")