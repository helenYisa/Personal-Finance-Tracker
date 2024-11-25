# Personal Finance Tracker

This is a Django-based web application designed to help users track their personal finances. The system enables users to manage their income, expenses, and categories while providing dynamic visualizations of their financial data. It includes features like adding, deleting, and categorizing transactions and filtering data by date.

## System Components

### Dashboard

**Description**: Provides an overview of the user's financial data, including total income, total expenses, and total balance. Displays visualizations such as income vs. expenses and expense distribution charts.
Key Features:
    Dynamic charts for income and expenses.
    Yearly and monthly filtering.

## Income

**Description**: Allows users to add income records, including details like the amount, description, and date.
Key Features:
    Add new income entries.
    Delete existing income records.
    View filtered income data.

## Expenses

**Description**: Enables users to add expense records, categorize them, and view expense details.
Key Features:
    Add new expense entries with a category.
    Delete existing expense records.
    Filter expenses by date or category.

## Categories

**Description**: Manages expense categories to organize spending more effectively.
Key Features:
    Add custom categories with a name and description.
    Use categories in expense entries.

## Authentication

**Description**: Ensures secure access to user-specific data with user authentication.
Key Features:
    User registration and login.
    Logout functionality.
    Password validation and security.

## Visualization

**Description**: Displays financial data through dynamic charts to help users analyze their finances visually.
Key Features:
    Pie chart for expenses by category.
    Bar chart for monthly income vs. expenses.

## Features

**Add Income and Expenses**: Users can record income and expense transactions with relevant details.
**Categorize Expenses**: Categorize spending to understand spending patterns better.
**View Totals and Balance**: See the total income, expenses, and remaining balance.
**Filter Data**: Filter financial data by year and month.
Visualize Data: View charts that represent financial data dynamically.
**Delete Records**: Delete income or expense entries to correct errors or update records.

## Requirements

Python 3.8 or later
Django 4.x
Bootstrap 5
matpoltlib (or equivalent library for visualizations)

## Setup

1. Clone the repository to your local machine:
   ```bash
    git clone https://github.com/yourusername/personal-finance-tracker.git
    cd personal-finance-tracker

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Configure the database:
    Run migrations:
    ```bash
    python manage.py migrate

4. Start the development server:
   ```bash
   python manage.py runserver

5. Open the application in your web browser at 
   http://127.0.0.1:8000.

## Usage

1. **Register and Login**: Create an account or log in with your credentials.
2. **Add Income**: Navigate to the Dashboard page  to "Add Income" to record income transactions.
3. **Add Expenses**: Use the "Add Expense" page to log expenses and assign categories.
4. **View Dashboard**: Check the dashboard for an overview of your finances and dynamic charts.
5. **Manage Categories**: Add new categories to organize expenses effectively.
6. **Delete Records**: Use the delete functionality to remove incorrect entries.