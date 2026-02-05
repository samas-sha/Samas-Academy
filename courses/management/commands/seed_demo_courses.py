from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Seed demo courses for production or testing.'

    def handle(self, *args, **options):
        demo_courses = [
            {'name': 'Python Basics', 'description': 'Learn Python from scratch.'},
            {'name': 'Web Development', 'description': 'Build websites with Django.'},
            {'name': 'Data Science', 'description': 'Intro to data analysis and ML.'},
            {'name': 'JavaScript Essentials', 'description': 'JS for beginners.'},
            {'name': 'Database Design', 'description': 'Learn SQL and DB modeling.'},
        ]
        created = 0
        for course in demo_courses:
            obj, was_created = Course.objects.get_or_create(name=course['name'], defaults={'description': course['description']})
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'{created} demo courses added.'))
