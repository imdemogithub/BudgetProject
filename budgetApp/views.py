from django.shortcuts import render, redirect
from .models import *
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.db.utils import IntegrityError
import os
# Create your views here.

default_data = {}
default_data['gender_choice_options'] = []
default_data['month_choice_options'] = []

for k,v in gender_choices:
    g = {
        'short_k': k,
        'text': v,
    }
    default_data['gender_choice_options'].append(g)

for month_num,month_name in month_choices:
    g = {
        'month_num': month_num,
        'month_name': month_name,
    }
    default_data['month_choice_options'].append(g)

print(default_data['gender_choice_options'])    
print(default_data['month_choice_options'])

def index(request):
    return redirect(signin_page)
    # return render(request, 'index.html', default_data)

def signup_page(request):
    return render(request, 'signup_page.html')

def signin_page(request):
    return render(request, 'signin_page.html')

def forgot_pwd_page(request):
    return render(request, 'forgot_pwd_page.html')

def otp_page(request):
    return render(request, 'otp_page.html')

# OTP Creation
def otp(request):
    otp_number = randint(1000, 9999)
    print("OTP is: ", otp_number)
    request.session['otp'] = otp_number

# send_otp
def send_otp(request, otp_for="register"):
    print(otp_for)
    otp(request)

    email_to_list = [request.session['reg_data']['email'],]

    if otp_for == 'activate':
        request.session['otp_for'] = 'activate'
        subject = f'OTP for Budget Account Activation'
    elif otp_for == 'recover_pwd':
        request.session['otp_for'] = 'recover_pwd'
        subject = f'OTP for Budget Password Recovery'
    else:
        request.session['otp_for'] = 'register'
        subject = f'OTP for Budget Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {request.session['otp']}."

    send_mail(subject, message, email_from, email_to_list)


# verify otp
def verify_otp(request, verify_for="register"):

    if request.session['otp'] == int(request.POST['otp']):

        if verify_for == 'activate':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            # master.Password = request.session['reg_data']['password']
            master.IsActive = True
            master.save()


            return redirect(profile_page)
        elif verify_for == 'recover_pwd':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            master.Password = request.session['reg_data']['password']
            master.save()
        else:
            print('before new account')
            master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
            )

            UserProfile.objects.create(
                Master = master,
            )
            print('after new account')

        print("verified.")
        del request.session['reg_data']

    else:
        print("Invalid OTP")
        
        return redirect(otp_page)
    
    return redirect(signin_page)



def profile_page(request):
    if 'email' in request.session:
        profile_data(request) # load profile data
        load_expense_category() # load expense categories
        # load_budgets(request) # load all budgets
        # load_expsenses(request) # load all expenses

        budget_expense(request) # combined data
        return render(request, 'profile_page.html', default_data)
    
    return redirect(signin_page)

# load expense category
def load_expense_category():
    exp_categories = ExpenseCategory.objects.all()
    default_data['exp_categories'] = exp_categories

# load budgets
def load_budgets(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    all_budgets = Budget.objects.filter(UserProfile = user_profile)

    for budget in all_budgets:
        # print('year', budget.CreatedOn)
        for month_ch in default_data['month_choice_options']:
            if month_ch['month_num'] == budget.BudgetMonth:
                budget.MonthName = month_ch['month_name']

    default_data['my_budgets'] = all_budgets[::-1]

# load expenses
def load_expsenses(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    all_expsenses = Expense.objects.filter(UserProfile = user_profile)
    
    for expsens in all_expsenses:
        # print('year', budget.CreatedOn)
        for month_ch in default_data['month_choice_options']:
            
            if month_ch['month_num'] == expsens.Date.month:
                expsens.MonthName = month_ch['month_name']

    
    default_data['all_expsenses'] = all_expsenses[::-1]

# budget and expenses calculation
def budget_expense(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    all_budgets = Budget.objects.filter(UserProfile = user_profile)

    
    month = 0
    total_used = 0
    # budget_amt = 0
    
    budget_expenses = []
    
    for budget in all_budgets:
        total_exp = 0
        exps = Expense.objects.filter(Budget = budget)
        for exp in exps:
            total_exp += exp.Amount
            exp.Percentage = (exp.Amount / budget.Amount) * 100

            for month_ch in default_data['month_choice_options']:
            
                if month_ch['month_num'] == exp.Date.month:
                    exp.MonthName = month_ch['month_name']
        
        budget_expenses.append({
            'budget': budget,
            'expenses': exps,
            'remaining': budget.Amount - total_exp,
            'total_exp': total_exp,
            'percentage': (total_exp / budget.Amount) * 100,
            'month': budget.BudgetMonth,
        })
    print(budget_expenses)
    default_data['budget_expenses'] = budget_expenses[::-1]
        
# forgot pwd functionality
def forgot_password(request):
    try:
        Master.objects.get(Email=request.POST['email'])

        password = request.POST['password']
        if password == request.POST['confirm_password']:
            request.session['reg_data'] = {
                'email': request.POST['email'],
                'password': password,
            }

            send_otp(request, otp_for="recover_pwd")

            print('OTP sent successfully for recover password.')

            return redirect(otp_page)
        else:
            print('both password should be same.')

    except Master.DoesNotExist as err:
        print('email not registered.')

        return redirect(signup_page)

    return redirect(forgot_pwd_page)

# register view
def signup(request):
    try:
        masters = Master.objects.all()
        for master in masters:
            if request.POST['email'] == master.Email:
                raise IntegrityError

        password = request.POST['password']
        if password == request.POST['confirm_password']:
            request.session['reg_data'] = {
                'email': request.POST['email'],
                'password': password,
            }

            send_otp(request)

            print('OTP sent successfully.')

            return redirect(otp_page)
        else:
            print('both password should be same.')

    except IntegrityError as err:
        print(err)
        print('email already exist. please login.')
    
        return redirect(signin_page)

    return redirect(signup_page)

# signup functionality
def signups(request):
    print(request.POST)
    password = request.POST['password']

    if password == request.POST['confirm_password']:
        master = Master.objects.create(Email = request.POST['email'], Password = password)
        UserProfile.objects.create(Master = master)

        print('Signup successfully.')
    else:
        print('both password should be same.')
        return redirect(signup_page)

    return redirect(signin_page)



# load profile data
def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    user_profile.first_name = user_profile.FullName.split()[0]
    user_profile.last_name = user_profile.FullName.split()[1]

    user_profile.BirthDate = user_profile.BirthDate.strftime("%Y-%m-%d")

    default_data['user_data'] = user_profile

# signin functionality
def signin(request):
    print(request.POST)
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            if master.IsActive:
                request.session['email'] = master.Email
                return redirect(profile_page)
            else:
                print('You entered wrong password.')
        else:
            request.session['reg_data'] = {
                'email': request.POST['email'],
                'password': request.POST['password'],
            }
            print('Inactive user.')
            send_otp(request, otp_for='activate')
            return redirect(otp_page)

    except Master.DoesNotExist as err:
        print(f'{request.POST["email"]} not registered.')
    
    return redirect(signin_page)

main_path = settings.MEDIA_ROOT


# profile update functionality
def profile_update(request):
    print(request.POST)
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)

    user_profile.FullName = ' '.join([request.POST['first_name'], request.POST['last_name']])
    user_profile.Mobile = request.POST['mobile']
    user_profile.Gender = request.POST['gender']
    user_profile.BirthDate = request.POST['birth_date']
    user_profile.Address = request.POST['address']

    
    file_path = os.path.join(main_path, 'profiles')

    


    if 'profile_image' in request.FILES:
        file = request.FILES['profile_image']
        
        new_name = f"{user_profile.id}_{user_profile.Master.Email.split('@')[0]}.{file.name.split('.')[-1]}"
        file.name = new_name

        for f in os.scandir(file_path):
            if f.name == file.name:
                print('same files')
                os.unlink(os.path.join(file_path, file.name))                

        user_profile.ProfileImage = file

    user_profile.save()

    return redirect(profile_page)

# Password reset
def password_reset(request):
    master = Master.objects.get(Email = request.session['email'])
    if master.Password == request.POST['current_password']:
        if request.POST['new_password'] == request.POST['confirm_password']:
            master.Password = request.POST['new_password']
            master.save()
        else:
            print('both password should be same.')
    else:
        print('password does not matched.')
    return redirect(profile_page)

# add new budget functionality
def add_budget(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = UserProfile.objects.get(Master = master)

    Budget.objects.create(UserProfile = profile, BudgetMonth=request.POST['budget_month'], Amount=request.POST['budget_amount'])

    print('budget added.')


    return redirect(profile_page)

# add new expense functionality
def add_expsense(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = UserProfile.objects.get(Master = master)

    budget_id = int(request.POST['budget_name'])
    exp_category_id = int(request.POST['exp_category'])

    budget = Budget.objects.get(id=budget_id)
    exp_category = ExpenseCategory.objects.get(id=exp_category_id)

    Expense.objects.create(
        ExpenseCategory = exp_category,
        Budget = budget,
        UserProfile = profile,
        Amount = request.POST['expense_amount'],
        Date = request.POST['expense_date'],
        Description = request.POST['exp_description'],
    )

    print('expense added.')


    return redirect(profile_page)

# logout functionality
def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect(signin_page)
    
    return redirect(profile_page)

# temp
def get_expenses(request):
    master = Master.objects.get(Email = '')
    profile = UserProfile.objects.get(Master = master)
    expenses = Expense.objects.filter(UserProfile = profile)