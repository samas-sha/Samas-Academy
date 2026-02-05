"""
Seed sample departments for development.
Usage: python manage.py seed_departments
"""
from django.core.management.base import BaseCommand
from students.models import Department


class Command(BaseCommand):
    help = 'Creates sample departments'

    def handle(self, *args, **options):
        departments = [
            ('Computer Science', 'CS'),
            ('Mathematics', 'MATH'),
            ('Physics', 'PHY'),
            ('Chemistry', 'CHEM'),
            ('English', 'ENG'),
        ]
        for name, code in departments:
            dept, created = Department.objects.get_or_create(code=code, defaults={'name': name})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {name}'))
        self.stdout.write(self.style.SUCCESS('Departments seeded.'))
