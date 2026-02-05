"""
Management command to create the initial admin user.
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Creates an admin user with UserProfile for the Student Management System'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@school.edu', help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
        else:
            self.stdout.write(f'User {username} already exists.')

        profile, prof_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'admin'}
        )
        if prof_created:
            self.stdout.write(self.style.SUCCESS(f'Created admin profile for {username}'))
        else:
            if profile.role != 'admin':
                profile.role = 'admin'
                profile.save()
                self.stdout.write(self.style.SUCCESS(f'Updated profile to admin for {username}'))

        self.stdout.write(self.style.SUCCESS(f'Admin login: username={username}, password={password}'))
