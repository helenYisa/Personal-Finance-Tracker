from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Represents a category for expenses.
    
    Attributes:
        name (str): The name of the category.
        description (str): A detailed description of the category.
    """
    name = models.CharField(max_length=100)  # Category name, max length of 100 characters
    description = models.TextField()  # Detailed description of the category

    def __str__(self):
        """
        Returns a string representation of the category.
        """
        return f"{self.name}: {self.description}"


class Expense(models.Model):
    """
    Represents an expense entry for a user.
    
    Attributes:
        user (User): The user associated with the expense.
        category (Category): The category the expense falls under.
        amount (Decimal): The amount spent.
        description (str): A description of the expense.
        date (Date): The date the expense was made.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the expense to a user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Links the expense to a category
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Expense amount
    description = models.TextField()  # Detailed description of the expense
    date = models.DateField()  # Date of the expense

    def __str__(self):
        """
        Returns a string representation of the expense.
        """
        return f"{self.category.name}: {self.amount}"


class Income(models.Model):
    """
    Represents an income entry for a user.
    
    Attributes:
        user (User): The user associated with the income.
        amount (Decimal): The amount of income.
        description (str): A description of the income.
        date (Date): The date the income was received.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the income to a user
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Income amount
    description = models.TextField()  # Detailed description of the income
    date = models.DateField()  # Date of the income