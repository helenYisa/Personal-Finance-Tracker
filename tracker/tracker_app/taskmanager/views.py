from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ExpenseForm, IncomeForm
from .models import Expense, Income
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import date
import base64
from .models import Category
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        return redirect('expenses')  # Redirect to a list view of categories
    return render(request, 'add_category.html')


def delete_category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect('dashboard')  # Redirect to a list view of categories


def expenses(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expenses_instance = form.save(commit=False)
            expenses_instance.user = request.user  # Assign the user to the income instance
            expenses_instance.save()
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = ExpenseForm()
    return render(request, 'expenses.html', {'expense_form': form})


def income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income_instance = form.save(commit=False)
            income_instance.user = request.user  # Assign the user to the income instance
            income_instance.save()
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = IncomeForm()  # Define the form for GET requests

    return render(request, 'income.html', {'income_form': form})



@login_required
def dashboard(request):
    # Default filters
    today = date.today()
    filter_year = request.GET.get('year', '')  # Default to empty if not provided
    filter_month = request.GET.get('month', '')  # Default to empty if not provided

    # Validate and convert to integers if possible
    try:
        filter_year = int(filter_year) if filter_year else None
    except ValueError:
        filter_year = None

    try:
        filter_month = int(filter_month) if filter_month else None
    except ValueError:
        filter_month = None

    # Filter expenses and income
    user_expenses = Expense.objects.filter(user=request.user)
    user_income = Income.objects.filter(user=request.user)

    if filter_year:
        user_expenses = user_expenses.filter(date__year=filter_year)
        user_income = user_income.filter(date__year=filter_year)

    if filter_month:
        user_expenses = user_expenses.filter(date__month=filter_month)
        user_income = user_income.filter(date__month=filter_month)

    # Initialize totals
    total_expenses = 0
    total_income = 0
    total_balance = 0

    # Filter expenses and income only if a valid year is selected
    if filter_year:
        user_expenses = Expense.objects.filter(user=request.user, date__year=filter_year)
        user_income = Income.objects.filter(user=request.user, date__year=filter_year)

        if filter_month:
            user_expenses = user_expenses.filter(date__month=filter_month)
            user_income = user_income.filter(date__month=filter_month)

        # Calculate totals
        total_expenses = sum(expense.amount for expense in user_expenses)
        total_income = sum(income.amount for income in user_income)

    # Calculate balance
    total_balance = total_income - total_expenses

    # Generate Pie Chart for Expenses by Category
    category_totals = {}
    if filter_year:  # Only generate the chart if a year is selected
        if filter_month:
            filtered_expenses = user_expenses.filter(date__year=filter_year, date__month=filter_month)
        else:
            filtered_expenses = user_expenses.filter(date__year=filter_year)

        for expense in filtered_expenses:
            category_name = expense.category.name
            category_totals[category_name] = category_totals.get(category_name, 0) + expense.amount

    fig, ax = plt.subplots()
    if category_totals:
        ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title('Expense Distribution')
    else:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    pie_chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Generate Grouped Bar Chart for Monthly Income vs Expenses
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_expenses = [0] * 12
    monthly_income = [0] * 12

    if filter_year:
        for expense in Expense.objects.filter(user=request.user, date__year=filter_year):
            monthly_expenses[expense.date.month - 1] += expense.amount

        for income in Income.objects.filter(user=request.user, date__year=filter_year):
            monthly_income[income.date.month - 1] += income.amount

    fig, ax = plt.subplots()

    x = range(len(months))  # Positions for the months
    width = 0.35  # Width of each bar

    # Plotting bars for income and expenses
    ax.bar([i - width / 2 for i in x], monthly_income, width, label='Income', color='green', alpha=0.7)
    ax.bar([i + width / 2 for i in x], monthly_expenses, width, label='Expenses', color='red', alpha=0.7)

    # Labels and title
    ax.set_title('Monthly Income vs Expenses')
    ax.set_xlabel('Months')
    ax.set_ylabel('Amount')
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    bar_chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Pass data to the template
    return render(request, 'dashboard.html', {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'total_balance': total_balance,
        'pie_chart_data': pie_chart_data,
        'bar_chart_data': bar_chart_data,
        'filter_year': filter_year,
        'filter_month': filter_month,
        'expense_form': ExpenseForm(),
        'income_form': IncomeForm(),
        'years': range(2020, today.year + 1),
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    })

