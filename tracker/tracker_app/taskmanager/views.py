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
from decimal import Decimal
import json


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        Category.objects.create(name=name, description=description)
        return redirect("expenses")  # Redirect to a list view of categories
    return render(request, "add_category.html")


def delete_category(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect("dashboard")  # Redirect to a list view of categories


def expenses(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expenses_instance = form.save(commit=False)
            expenses_instance.user = (
                request.user
            )  # Assign the user to the income instance
            expenses_instance.save()
            return redirect("dashboard")  # Redirect to the dashboard
    else:
        form = ExpenseForm()
    return render(request, "expenses.html", {"expense_form": form})


def income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income_instance = form.save(commit=False)
            income_instance.user = (
                request.user
            )  # Assign the user to the income instance
            income_instance.save()
            return redirect("dashboard")  # Redirect to the dashboard
    else:
        form = IncomeForm()  # Define the form for GET requests

    return render(request, "income.html", {"income_form": form})


# Custom serializer for Decimal values
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


@login_required
def dashboard(request):
    today = date.today()
    filter_year = request.GET.get("year", "")
    filter_month = request.GET.get("month", "")

    # Validate and convert to integers

    filter_year = int(filter_year) if filter_year else None

    filter_month = int(filter_month) if filter_month else None

    # Fetch data
    user_expenses = Expense.objects.filter(user=request.user, date__year=filter_year)
    user_income = Income.objects.filter(user=request.user, date__year=filter_year)

    if filter_month:
        user_expenses = user_expenses.filter(date__month=filter_month)
        user_income = user_income.filter(date__month=filter_month)

    total_expenses = sum(expense.amount for expense in user_expenses)
    total_income = sum(income.amount for income in user_income)
    total_balance = total_income - total_expenses

    # Prepare data for the pie chart (category-wise expense distribution)
    category_totals = {}
    for expense in user_expenses:
        category_name = expense.category.name
        category_totals[category_name] = (
            category_totals.get(category_name, 0) + expense.amount
        )

    pie_chart_data = {
        "labels": list(category_totals.keys()),
        "datasets": [
            {
                "data": list(category_totals.values()),
                "backgroundColor": [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                    "#9966FF",
                    "#FF9F40",
                ],
            }
        ],
    }

    # Prepare data for the bar chart (monthly income vs expenses)
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    monthly_expenses = [0] * 12
    monthly_income = [0] * 12

    for expense in user_expenses:
        monthly_expenses[expense.date.month - 1] += expense.amount

    for income in user_income:
        monthly_income[income.date.month - 1] += income.amount

    bar_chart_data = {
        "labels": months,
        "datasets": [
            {
                "label": "Income",
                "data": monthly_income,
                "backgroundColor": "rgba(75, 192, 192, 0.7)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            },
            {
                "label": "Expenses",
                "data": monthly_expenses,
                "backgroundColor": "rgba(255, 99, 132, 0.7)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 1,
            },
        ],
    }

    # Pass data to the template
    return render(
        request,
        "dashboard.html",
        {
            "total_expenses": total_expenses,
            "total_income": total_income,
            "total_balance": total_balance,
            "pie_chart_data": json.dumps(pie_chart_data, default=decimal_default),
            "bar_chart_data": json.dumps(bar_chart_data, default=decimal_default),
            "filter_year": filter_year,
            "filter_month": filter_month,
            "years": range(2020, today.year + 1),
            "months": months,
        },
    )
