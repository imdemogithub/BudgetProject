from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = admin.site.site_title = 'Budgetry'

all_models = [Budget, Expense, ExpenseCategory, Master, MemberCategory, MemberList, SharedExpense, UserProfile]
for md in all_models:
    admin.site.register(md)