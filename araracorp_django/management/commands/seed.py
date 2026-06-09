from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from araracorp_django.models import Category, MenuItem, Table

class Command(BaseCommand):
    help = 'Seed the database'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admincorp@gmail.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser Created'))
        else :
            self.stdout.write('Superuser already exist, sipping...')

        beverages, _ = Category.objects.get_or_create(name= 'Beverages')
        main_course, _ = Category.objects.get_or_create(name = 'Main Course')
        snacks, _ = Category.objects.get_or_create(name = 'Snacks')

        MenuItem.objects.get_or_create(
            name = 'Es Teh', defaults={'category': beverages, 'price': 2000, 'description': 'Iced Tea'}
        )
        MenuItem.objects.get_or_create(
            name = 'Nasi Goreng', defaults={'category': main_course, 'price': 10000, 'description': 'Gorgor gorengggg'}
        )
        MenuItem.objects.get_or_create(
            name = 'Mie Nyemek', defaults={'category': main_course, 'price': 10000, 'description': 'Nyemekin aja bre'}
        )
        MenuItem.objects.get_or_create(
            name = 'Piscok', defaults={'category': snacks, 'price': 5000, 'description': 'Pisang berlapis coklat'}
        )

        for i in range(1, 6):
            Table.objects.get_or_create(number= i)
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully: '))