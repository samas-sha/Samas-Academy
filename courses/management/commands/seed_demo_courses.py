from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Seed demo courses for production or testing.'

    def handle(self, *args, **options):
        demo_courses = [
            {'name': 'Python Basics', 'code': 'PY101'},
            {'name': 'Web Development', 'code': 'WD201'},
            {'name': 'Data Science', 'code': 'DS301'},
            {'name': 'JavaScript Essentials', 'code': 'JS102'},
            {'name': 'Database Design', 'code': 'DB202'},
        ]
        created = 0
        for course in demo_courses:
            self.stdout.write(f'Processing course: {course}')
            obj, was_created = Course.objects.get_or_create(name=course['name'], code=course['code'])
            if was_created:
                self.stdout.write(self.style.SUCCESS(f'Created: {course["name"]} ({course["code"]})'))
                created += 1
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {course["name"]} ({course["code"]})'))
        self.stdout.write(self.style.SUCCESS(f'{created} demo courses added.'))
