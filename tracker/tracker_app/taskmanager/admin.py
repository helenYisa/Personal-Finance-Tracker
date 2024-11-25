from django.contrib import admin
from .models import Category, Expense, Income


# Admin configuration for the Category model
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.

    Features:
    - Displays name and description in the admin list view.
    - Allows search functionality by category name.
    """
    list_display = ('name', 'description')  # Fields to display in the list view
    search_fields = ('name',)  # Fields searchable in the admin panel


# Register the Category model with its admin configuration
admin.site.register(Category, CategoryAdmin)


# Admin configuration for the Expense model
class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Expense model.

    Features:
    - Displays user, category, amount, and date in the list view.
    - Filters by category and date for better navigation.
    - Search functionality for category name and description.
    """
    list_display = ('user', 'category', 'amount', 'date')  # Fields to display in the list view
    list_filter = ('category', 'date')  # Filters for narrowing down data
    search_fields = ('category__name', 'description')  # Fields searchable in the admin panel


# Register the Expense model with its admin configuration
admin.site.register(Expense, ExpenseAdmin)


# Admin configuration for the Income model
class IncomeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Income model.

    Features:
    - Displays user, amount, and date in the list view.
    - Filters by date for easy navigation.
    - Search functionality by description.
    """
    list_display = ('user', 'amount', 'date')  # Fields to display in the list view
    list_filter = ('date',)  # Filters for narrowing down data
    search_fields = ('description',)  # Fields searchable in the admin panel


# Register the Income model with its admin configuration
admin.site.register(Income, IncomeAdmin)
