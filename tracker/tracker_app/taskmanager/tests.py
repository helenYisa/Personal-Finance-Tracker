from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Expense, Income
from datetime import date


class CategoryModelTest(TestCase):
    """
    Test cases for the Category model.
    """
    def setUp(self):
        # Set up a sample category for testing
        self.category = Category.objects.create(name="Food", description="Expenses related to food and dining")

    def test_category_creation(self):
        # Check if the category is created successfully
        self.assertEqual(self.category.name, "Food")
        self.assertEqual(self.category.description, "Expenses related to food and dining")

    def test_category_str_method(self):
        # Test the string representation of the category
        self.assertEqual(str(self.category), "Food: Expenses related to food and dining")


class ExpenseModelTest(TestCase):
    """
    Test cases for the Expense model.
    """
    def setUp(self):
        # Set up user, category, and expense objects for testing
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Transport", description="Travel expenses")
        self.expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=50.00,
            description="Taxi fare",
            date=date.today()
        )

    def test_expense_creation(self):
        # Check if the expense is created successfully
        self.assertEqual(self.expense.user, self.user)
        self.assertEqual(self.expense.category, self.category)
        self.assertEqual(self.expense.amount, 50.00)
        self.assertEqual(self.expense.description, "Taxi fare")
        self.assertEqual(self.expense.date, date.today())

    def test_expense_str_method(self):
        # Test the string representation of the expense
        self.assertEqual(str(self.expense), "Transport: 50.00")


class IncomeModelTest(TestCase):
    """
    Test cases for the Income model.
    """
    def setUp(self):
        # Set up user and income objects for testing
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.income = Income.objects.create(
            user=self.user,
            amount=200.00,
            description="Freelance project",
            date=date.today()
        )

    def test_income_creation(self):
        # Check if the income is created successfully
        self.assertEqual(self.income.user, self.user)
        self.assertEqual(self.income.amount, 200.00)
        self.assertEqual(self.income.description, "Freelance project")
        self.assertEqual(self.income.date, date.today())

    def test_income_str_method(self):
        # Test the string representation of the income
        self.assertEqual(str(self.income), "Income: 200.00")
