from .models import Manage_Budget
from django import forms


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Manage_Budget
        fields = ["amount", "date"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={"class": "bg-gray-700 w-full rounded p-2 my-3"}
            ),
            "date": forms.DateInput(
                attrs={"type": "date", "class": "bg-gray-700 w-full rounded p-2 my-3"}
            ),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Manage_Budget
        fields = ["amount", "category", "date"]
        widgets = {
            "category": forms.TextInput(
                attrs={"class": "bg-gray-700 w-full rounded p-2 my-3"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "bg-gray-700 w-full rounded p-2 my-3"}
            ),
            "date": forms.DateInput(
                attrs={"type": "date", "class": "bg-gray-700 w-full rounded p-2 my-3"}
            ),
        }
