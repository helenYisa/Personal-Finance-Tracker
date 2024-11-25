from django import forms
from django.contrib.auth.models import User
from .models import Expense, Income, Category


class SignUpForm(forms.ModelForm):
    """
    A custom form for user registration.
    
    Features:
    - Includes a password field with input masking (PasswordInput widget).
    - Saves the password securely using Django's `set_password` method.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """
        Meta class specifying the model and fields to include in the form.
        """
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        """
        Save method overridden to hash the user's password before saving.
        """
        user = super().save(commit=False)  # Get the user instance without saving it yet
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:  # Save the user if commit is True
            user.save()
        return user


class ExpenseForm(forms.ModelForm):
    """
    A form for creating and updating Expense instances.
  
    Features:
    - Allows the user to select a category from existing categories.
    - Includes custom widgets for styling the input fields.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",  # Placeholder text for the dropdown
        widget=forms.Select(attrs={'class': 'custom-select-field'}),
    )

    class Meta:
        """
        Meta class specifying the model, fields, and custom widgets for the form.
        """
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),  # Dropdown for category
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),  # Numeric input for amount
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea for description
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Date picker
        }


class IncomeForm(forms.ModelForm):
    """
    A form for creating and updating Income instances.
    
    Features:
    - Uses custom widgets for styling the input fields.
    """
    class Meta:
        """
        Meta class specifying the model, fields, and custom widgets for the form.
        """
        model = Income
        fields = ['amount', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),  # Numeric input for amount
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea for description
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Date picker
        }
