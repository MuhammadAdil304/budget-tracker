from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from manage_budget.models import Manage_Budget
from manage_budget.forms import ExpenseForm, IncomeForm
import json


@login_required(login_url="/login/")
def index(request):
    user = request.user
    total_budget = Manage_Budget.claculate_balance(user=user)
    show_expenses = Manage_Budget.objects.filter(  ## pylint: disable=no-member
        user=request.user, transaction="expense"
    ).order_by("-created_at")

    total_income = total_budget["total_income"]
    total_expense = total_budget["total_expense"]
    total_balance = total_budget["total_balance"]
    expenses_by_category = total_budget["expense_by_category"]
    expenses_with_percentage = []
    for expense in expenses_by_category:
        if total_expense > 0:
            percentage = (expense["total"] / total_expense) * 100
        else:
            percentage = 0
        expenses_with_percentage.append(
            {
                "category": expense["category"],
                "total": expense["total"],
                "percentage": round(min(percentage, 100), 2),
            }
        )

    chart_data = {
        "income": str(total_income),
        "expense": str(total_expense),
        "balance": str(total_balance),
    }
    print("expenses_with_percentage", expenses_with_percentage)

    context = {
        "total_budget": total_budget,
        "expenses": show_expenses,
        "expense_by_category": expenses_with_percentage,
        "chart_data": json.dumps(chart_data),
    }
    return render(request, "index.html", context)


def addExpense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction = "expense"
            transaction.save()
            print(transaction)
            return redirect("/")
    else:
        form = ExpenseForm()
    return render(request, "addExpense.html", {"form": form})


def addIncome(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction = "income"
            transaction.save()
            print(transaction)
            print(form)
            return redirect("/")
    else:
        form = IncomeForm()
    return render(request, "addIncome.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials.")
            return redirect("/login/")
        login(request, user)
        return redirect("/")
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("/signup/")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

        user.set_password(password)
        user.save()

        return redirect("/login/")
    return render(request, "signup.html")
