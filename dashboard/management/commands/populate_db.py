from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Category, Product, Customer, Order, OrderItem
from accounts.models import Profile
from django.utils import timezone
from django.db import transaction
import random
from django.core.files.images import ImageFile
import os
from django.conf import settings
import datetime


class Command(BaseCommand):
    help = 'Ma\'lumotlar bazasini test ma\'lumotlar bilan to\'ldirish'

    def handle(self, *args, **kwargs):
        self.stdout.write('Ma\'lumotlar bazasini to\'ldirish boshlandi...')

        # Eski ma'lumotlarni tozalash
        self.stdout.write('Eski ma\'lumotlarni tozalash...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Customer.objects.all().delete()

        # Foydalanuvchilar yaratish
        self.create_users()

        # Kategoriyalar yaratish
        self.create_categories()

        # Mahsulotlar yaratish
        self.create_products()

        # Mijozlar yaratish
        self.create_customers()

        # Buyurtmalar yaratish
        self.create_orders()

        self.stdout.write(self.style.SUCCESS('Ma\'lumotlar bazasi muvaffaqiyatli to\'ldirildi!'))

    def create_users(self):
        self.stdout.write('Foydalanuvchilar yaratilmoqda...')

        # Admin foydalanuvchisi
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            admin_profile = Profile.objects.get(user=admin_user)
            admin_profile.phone = '+998901234567'
            admin_profile.position = 'Administrator'
            admin_profile.address = 'Toshkent, Uzbekistan'
            admin_profile.save()

        # Oddiy foydalanuvchilar
        users_data = [
            {
                'username': 'manager',
                'email': 'manager@example.com',
                'password': 'manager123',
                'first_name': 'Sardor',
                'last_name': 'Aliyev',
                'phone': '+998912345678',
                'position': 'Sotuv menejeri',
                'address': 'Toshkent, Chilonzor'
            },
            {
                'username': 'seller',
                'email': 'seller@example.com',
                'password': 'seller123',
                'first_name': 'Dilshod',
                'last_name': 'Karimov',
                'phone': '+998923456789',
                'position': 'Sotuvchi',
                'address': 'Toshkent, Yunusobod'
            },
            {
                'username': 'accountant',
                'email': 'accountant@example.com',
                'password': 'accountant123',
                'first_name': 'Nilufar',
                'last_name': 'Rahimova',
                'phone': '+998934567890',
                'position': 'Hisobchi',
                'address': 'Toshkent, Mirzo Ulug\'bek'
            }
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                profile = Profile.objects.get(user=user)
                profile.phone = user_data['phone']
                profile.position = user_data['position']
                profile.address = user_data['address']
                profile.save()

    def create_categories(self):
        self.stdout.write('Kategoriyalar yaratilmoqda...')

        categories_data = [
            {
                'name': 'Ko\'ylaklar',
                'description': 'Erkaklar va ayollar uchun ko\'ylaklar'
            },
            {
                'name': 'Shimlar',
                'description': 'Erkaklar va ayollar uchun shimlar'
            },
            {
                'name': 'Kostyumlar',
                'description': 'Erkaklar uchun kostyumlar'
            },
            {
                'name': 'Ko\'ylaklari',
                'description': 'Ayollar uchun ko\'ylaklar'
            },
            {
                'name': 'Poyabzallar',
                'description': 'Erkaklar va ayollar uchun poyabzallar'
            },
            {
                'name': 'Aksessuarlar',
                'description': 'Soatlar, sumkalar, kamarlar va boshqalar'
            },
            {
                'name': 'Sport kiyimlari',
                'description': 'Sport uchun kiyimlar'
            }
        ]

        for category_data in categories_data:
            Category.objects.create(**category_data)

    def create_products(self):
        self.stdout.write('Mahsulotlar yaratilmoqda...')

        categories = Category.objects.all()

        products_data = [
            # Ko'ylaklar
            {
                'name': 'Klassik oq ko\'ylak',
                'description': 'Erkaklar uchun klassik oq ko\'ylak, 100% paxta',
                'price': 150000,
                'stock': 50,
                'category': categories.get(name='Ko\'ylaklar')
            },
            {
                'name': 'Biznes ko\'ylak',
                'description': 'Erkaklar uchun biznes ko\'ylak, ko\'k rangda',
                'price': 180000,
                'stock': 30,
                'category': categories.get(name='Ko\'ylaklar')
            },
            {
                'name': 'Casual ko\'ylak',
                'description': 'Erkaklar uchun casual ko\'ylak, turli ranglar',
                'price': 120000,
                'stock': 45,
                'category': categories.get(name='Ko\'ylaklar')
            },

            # Shimlar
            {
                'name': 'Klassik shim',
                'description': 'Erkaklar uchun klassik shim, qora rangda',
                'price': 220000,
                'stock': 25,
                'category': categories.get(name='Shimlar')
            },
            {
                'name': 'Jinsi shim',
                'description': 'Erkaklar va ayollar uchun jinsi shimlar',
                'price': 180000,
                'stock': 60,
                'category': categories.get(name='Shimlar')
            },
            {
                'name': 'Sport shim',
                'description': 'Sport uchun qulay shimlar',
                'price': 150000,
                'stock': 40,
                'category': categories.get(name='Shimlar')
            },

            # Kostyumlar
            {
                'name': 'Klassik kostyum',
                'description': 'Erkaklar uchun klassik kostyum, qora rangda',
                'price': 850000,
                'stock': 15,
                'category': categories.get(name='Kostyumlar')
            },
            {
                'name': 'Biznes kostyum',
                'description': 'Erkaklar uchun biznes kostyum, ko\'k rangda',
                'price': 950000,
                'stock': 10,
                'category': categories.get(name='Kostyumlar')
            },
            {
                'name': 'To\'y kostyumi',
                'description': 'To\'y marosimlari uchun maxsus kostyum',
                'price': 1200000,
                'stock': 8,
                'category': categories.get(name='Kostyumlar')
            },

            # Ayollar ko'ylaklari
            {
                'name': 'Yozgi ko\'ylak',
                'description': 'Ayollar uchun yozgi ko\'ylak, turli ranglar',
                'price': 250000,
                'stock': 35,
                'category': categories.get(name='Ko\'ylaklari')
            },
            {
                'name': 'Kechki ko\'ylak',
                'description': 'Ayollar uchun kechki tadbirlar uchun ko\'ylak',
                'price': 450000,
                'stock': 20,
                'category': categories.get(name='Ko\'ylaklari')
            },
            {
                'name': 'Biznes ko\'ylak',
                'description': 'Ayollar uchun biznes ko\'ylak',
                'price': 350000,
                'stock': 25,
                'category': categories.get(name='Ko\'ylaklari')
            },

            # Poyabzallar
            {
                'name': 'Klassik tufli',
                'description': 'Erkaklar uchun klassik qora tufli',
                'price': 350000,
                'stock': 30,
                'category': categories.get(name='Poyabzallar')
            },
            {
                'name': 'Sport poyabzal',
                'description': 'Sport uchun qulay poyabzal',
                'price': 280000,
                'stock': 45,
                'category': categories.get(name='Poyabzallar')
            },
            {
                'name': 'Ayollar tufli',
                'description': 'Ayollar uchun baland poshnali tufli',
                'price': 320000,
                'stock': 25,
                'category': categories.get(name='Poyabzallar')
            },

            # Aksessuarlar
            {
                'name': 'Erkaklar soati',
                'description': 'Erkaklar uchun biznes soat',
                'price': 550000,
                'stock': 15,
                'category': categories.get(name='Aksessuarlar')
            },
            {
                'name': 'Ayollar sumkasi',
                'description': 'Ayollar uchun charm sumka',
                'price': 420000,
                'stock': 20,
                'category': categories.get(name='Aksessuarlar')
            },
            {
                'name': 'Kamar',
                'description': 'Erkaklar uchun charm kamar',
                'price': 150000,
                'stock': 35,
                'category': categories.get(name='Aksessuarlar')
            },

            # Sport kiyimlari
            {
                'name': 'Sport futbolka',
                'description': 'Sport mashg\'ulotlari uchun futbolka',
                'price': 120000,
                'stock': 50,
                'category': categories.get(name='Sport kiyimlari')
            },
            {
                'name': 'Sport kostyum',
                'description': 'Sport uchun to\'liq kostyum',
                'price': 350000,
                'stock': 30,
                'category': categories.get(name='Sport kiyimlari')
            },
            {
                'name': 'Fitnes kiyimi',
                'description': 'Ayollar uchun fitnes kiyimi',
                'price': 280000,
                'stock': 40,
                'category': categories.get(name='Sport kiyimlari')
            }
        ]

        for product_data in products_data:
            Product.objects.create(**product_data)

    def create_customers(self):
        self.stdout.write('Mijozlar yaratilmoqda...')

        customers_data = [
            {
                'first_name': 'Alisher',
                'last_name': 'Usmanov',
                'phone': '+998901112233',
                'email': 'alisher@example.com',
                'address': 'Toshkent, Shayxontohur tumani, 15-uy'
            },
            {
                'first_name': 'Malika',
                'last_name': 'Karimova',
                'phone': '+998902223344',
                'email': 'malika@example.com',
                'address': 'Toshkent, Yunusobod tumani, 45-uy'
            },
            {
                'first_name': 'Jahongir',
                'last_name': 'Tursunov',
                'phone': '+998903334455',
                'email': 'jahongir@example.com',
                'address': 'Toshkent, Chilonzor tumani, 78-uy'
            },
            {
                'first_name': 'Nodira',
                'last_name': 'Azimova',
                'phone': '+998904445566',
                'email': 'nodira@example.com',
                'address': 'Toshkent, Mirzo Ulug\'bek tumani, 23-uy'
            },
            {
                'first_name': 'Rustam',
                'last_name': 'Qodirov',
                'phone': '+998905556677',
                'email': 'rustam@example.com',
                'address': 'Toshkent, Olmazor tumani, 56-uy'
            },
            {
                'first_name': 'Gulnora',
                'last_name': 'Rahimova',
                'phone': '+998906667788',
                'email': 'gulnora@example.com',
                'address': 'Toshkent, Yakkasaroy tumani, 34-uy'
            },
            {
                'first_name': 'Bobur',
                'last_name': 'Alimov',
                'phone': '+998907778899',
                'email': 'bobur@example.com',
                'address': 'Toshkent, Sergeli tumani, 12-uy'
            },
            {
                'first_name': 'Zarina',
                'last_name': 'Yusupova',
                'phone': '+998908889900',
                'email': 'zarina@example.com',
                'address': 'Toshkent, Bektemir tumani, 67-uy'
            },
            {
                'first_name': 'Dilshod',
                'last_name': 'Mahmudov',
                'phone': '+998909990011',
                'email': 'dilshod@example.com',
                'address': 'Toshkent, Uchtepa tumani, 89-uy'
            },
            {
                'first_name': 'Sabina',
                'last_name': 'Kamalova',
                'phone': '+998900001122',
                'email': 'sabina@example.com',
                'address': 'Toshkent, Yashnobod tumani, 43-uy'
            }
        ]

        for customer_data in customers_data:
            Customer.objects.create(**customer_data)

    def create_orders(self):
        self.stdout.write('Buyurtmalar yaratilmoqda...')

        customers = Customer.objects.all()
        products = Product.objects.all()
        users = User.objects.all()

        # So'nggi 30 kun ichida turli sanalarda buyurtmalar yaratish
        for _ in range(50):
            # Tasodifiy sana (so'nggi 30 kun ichida)
            days_ago = random.randint(0, 30)
            order_date = timezone.now() - datetime.timedelta(days=days_ago)

            # Tasodifiy mijoz va foydalanuvchi
            customer = random.choice(customers)
            user = random.choice(users)

            # Tasodifiy status
            status_choices = ['new', 'paid', 'delivered', 'cancelled']
            status_weights = [0.3, 0.4, 0.2, 0.1]  # Ehtimolliklar
            status = random.choices(status_choices, weights=status_weights, k=1)[0]

            # Buyurtma yaratish
            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer,
                    created_by=user,
                    status=status,
                    created_at=order_date,
                    note=f"{customer.first_name} {customer.last_name} uchun buyurtma"
                )

                # Buyurtmaga 1-5 ta mahsulot qo'shish
                num_items = random.randint(1, 5)
                selected_products = random.sample(list(products), num_items)

                for product in selected_products:
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity
                    )