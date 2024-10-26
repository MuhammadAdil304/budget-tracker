from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime

# Create your models here.
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTIONS_TYPE = [("income", "Income"), ("expense", "Expense")]
    transaction = models.CharField(choices=TRANSACTIONS_TYPE, max_length=20, default='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=50, default='')
    date = models.DateField(default= datetime.date.today)

    @classmethod
    def claculate_balance(cls, user):
        total_income = (
            Transactions.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="income"
            ).aggregate(Sum("amount"))["total"]
            or 0
        )
        total_expense = (
            Transactions.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="expense"
            ).aggregate(Sum("amount"))["total"]
            or 0
        )
        total_balance = total_income - total_expense
        expense_by_category = (
            Transactions.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="expense"
            )
            .values("category")
            .annotate(total=sum("amount"))
        )
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "total_balance": total_balance,
            "expense_by_category": expense_by_category,
        }
