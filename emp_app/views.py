from email import message
from pyexpat.errors import messages
from django.shortcuts import redirect, render, HttpResponse
from .models import Employee, Role, Department,User
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate,login as auth_login

from django.contrib.auth.decorators import login_required
from .models import LeaveApplication
from .forms import LeaveApplicationForm

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html',context)
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = request.POST['phone'] 
        dept = str(request.POST['dept']) 
        role = str(request.POST['role'])  
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=dept, 
            role=role,
            hire_date=datetime.now()
        )
        new_emp.save() 
        return HttpResponse('Employee added successfully.')
    
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")


def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')

def attendance(request):
    return render(request, 'attendance.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("User already exists")
        
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        new_user.set_password(password)
        new_user.save()

        return HttpResponse("User added successfully")
    elif request.method == 'GET':
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def dashboard(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    roles = Role.objects.all()
    total_employees = employees.count()
    total_departments = departments.count()
    total_roles = roles.count()

    context = {
        'employees': employees,
        'departments': departments,
        'roles': roles,
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_roles': total_roles
    }

    return render(request, 'dashboard.html', context)



@login_required
def apply_for_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.employee = request.user  # Assuming you have a relation to the user model
            leave_application.save()
            return redirect('leave_application_success')  # Redirect after a successful application
    else:
        form = LeaveApplicationForm()

    return render(request, 'apply_for_leave.html', {'form': form})


@login_required
def leave_application_success(request):
    return render(request, 'leave_application_success.html')