from django.db import models
import datetime

month_choices = []

for m in range(1, 13):
    d = datetime.date(2022, m, 1)
    
    month_choices.append((m, d.strftime("%B")))

# Create your models here.
class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    
    class Meta:
        db_table = "master"

    def __str__(self) -> str:
        return self.Email

gender_choices = (
    ('m', 'male'),
    ('f', 'female'),
)

class UserProfile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)

    ProfileImage = models.FileField(upload_to='profiles/', default='default_icon.png')
    UserName = models.CharField(max_length=25, default=str(), blank=True)
    FullName = models.CharField(max_length=25, default=str(), blank=True)
    Mobile = models.CharField(max_length=10, default=str(), blank=True)
    Gender = models.CharField(max_length=5, choices=gender_choices, default=str(), blank=True)
    BirthDate = models.DateField(default='2022-11-21')
    Address = models.TextField(max_length=100, default=str(), blank=True)

    class Meta:
        db_table = 'userprofile'

    def __str__(self) -> str:
        return self.FullName if self.FullName else self.Master.Email



class Budget(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    BudgetMonth = models.IntegerField(choices=month_choices)
    Amount = models.FloatField()
    CreatedOn = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Budget'
    
    def __str__(self) -> str:
        return f"Expense of month {self.BudgetMonth}"

class ExpenseCategory(models.Model):
    IconImage = models.FileField(upload_to='IconImages/', default='default_icon.png')
    Category = models.CharField(max_length=50)

    class Meta:
        db_table = 'ExpenseCategory'

    def __str__(self) -> str:
        return self.Category

class Expense(models.Model):
    ExpenseCategory = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    Amount = models.FloatField()
    Date = models.DateField()
    Description = models.TextField(max_length=100)

    class Meta:
        db_table = 'Expense'

    def __str__(self) -> str:
        return f"{self.ExpenseCategory.Category} | {self.UserProfile.UserName}"

class MemberCategory(models.Model):
    Title = models.CharField(max_length=25)

    class Meta:
        db_table = 'MemberCategory'

    def __str__(self) -> str:
        return self.Title

class MemberList(models.Model):
    MemberCategory = models.ForeignKey(MemberCategory, on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'MemberList'

    def __str__(self) -> str:
        return self.MemberCategory.Title

class SharedExpense(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    MemberList = models.ForeignKey(MemberList, on_delete=models.CASCADE)
    ExpenseCategory = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Date = models.DateField()
    Description = models.TextField(max_length=100)

    # can upload a expense reciept if you want to share.
    ExpenseReciept = models.FileField(upload_to='ExpenseReciept/', default='default.png')

    class Meta:
        db_table = 'SharedExpense'

    def __str__(self) -> str:
        return self.ExpenseCategory.Category