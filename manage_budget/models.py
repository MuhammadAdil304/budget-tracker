from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
import datetime

# Create your models here.
class Manage_Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTIONS_TYPE = [("income", "Income"), ("expense", "Expense")]
    transaction = models.CharField(choices=TRANSACTIONS_TYPE, max_length=20, default='income')
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    category = models.CharField(max_length=50, default='')
    date = models.DateField(default= timezone.now)
    created_at = models.DateTimeField(auto_now_add=True,)

    @classmethod
    def claculate_balance(cls, user):
        total_income = (
            Manage_Budget.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="income"
            ).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        total_expense = (
            Manage_Budget.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="expense"
            ).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        total_balance = total_income - total_expense
        expense_by_category = (
            Manage_Budget.objects.filter(  ## pylint: disable=no-member
                user=user, transaction="expense"
            )
            .values("category")
            .annotate(total=Sum("amount"))
        )
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "total_balance": total_balance,
            "expense_by_category": expense_by_category,
        }
