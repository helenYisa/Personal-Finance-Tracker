from django.core.management.base import BaseCommand
from taskmanager.models import Category


class Command(BaseCommand):
    help = "Seed the database with default categories"

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Housing", "description": "Rent, utilities, and maintenance."},
            {"name": "Transportation", "description": "Fuel, public transport, etc."},
            {"name": "Food & Dining", "description": "Groceries and dining out."},
            {"name": "Health & Fitness", "description": "Medical and wellness expenses."},
            {"name": "Entertainment", "description": "Movies, subscriptions, etc."},
        ]

        for category in categories:
            Category.objects.get_or_create(name=category["name"], defaults={"description": category["description"]})

        self.stdout.write(self.style.SUCCESS("Categories created successfully."))
