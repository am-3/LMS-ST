from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Employee, LeaveApl, generate_empid
from .forms import LeaveAplForm, EmployeeForm

# Admin check decorator
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied  # Raises a 403 Forbidden error
        return function(request, *args, **kwargs)
    return wrap

# Mapping dictionaries
leave_types = {
    'PER': 'Personal Leave',
    'OFI': 'Official Work',
    'PTO': 'Paid Time Off',
    'EMR': 'Emergency',
}

leave_statuses = {
    'SUB': 'Submitted',
    'ACP': 'Accepted',
    'REJ': 'Rejected',
    'DEF': 'Deferred',
}

def home(request):
    return render(request, "home.html")

def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admindashboard')  # Redirect to admin dashboard for superuser
        return redirect('home')  # Redirect to home for regular users

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admindashboard')  # Redirect to admin dashboard for superuser
            return redirect('home')  # Redirect to home for regular users
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create an Employee instance for the newly created user
            Employee.objects.create(user=user, empid=generate_empid(), name=user.username, email=user.email)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    empid = user.employee.id  # Assuming you have a relation to the Employee model

    # Fetch leave applications for the logged-in employee
    leave_applications = LeaveApl.objects.filter(empid=empid)

    # Statistics
    pending_leaves = leave_applications.filter(status='SUB').count()  # Pending status
    accepted_leaves = leave_applications.filter(status='ACP').count()  # Accepted status
    upcoming_leaves = leave_applications.filter(leaveDate__gt=timezone.now(), status='ACP').count()  # Accepted upcoming leaves

    context = {
        'user': user,
        'pending_leaves': pending_leaves,
        'accepted_leaves': accepted_leaves,
        'upcoming_leaves': upcoming_leaves,
        'leave_applications': leave_applications,
        'today': timezone.now().date(),  # Add today's date
    }
    
    return render(request, 'emp_dashboard.html', context)

@login_required
def apply(request):
    if request.method == "POST":
        form = LeaveAplForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)  # Create an instance but don't save it yet
            leave_application.empid = request.user.employee  # Set the employee field to the current user
            leave_application.save()  # Now save the instance
            messages.success(request, 'Leave application submitted successfully.')
            return redirect("/history")  # Redirect to the history page or another appropriate page
    else:
        form = LeaveAplForm()
        form.fields['empid'].initial = request.user.employee  # Set the initial value of empid

    return render(request, "apply.html", {'form': form})


@admin_required
def admindashboard(request):
    leave_applications = LeaveApl.objects.all()
    return render(request, "admin_dashboard.html", {'leave_applications': leave_applications})

@admin_required  # Ensure only admin users can access this
def update_leave_status(request, aplid):
    leave_application = get_object_or_404(LeaveApl, aplid=aplid)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['ACP', 'REJ']:
            leave_application.status = status
            leave_application.save()
            messages.success(request, f'Leave application {aplid} has been {"approved" if status == "ACP" else "rejected"}.')
            return redirect('admindashboard')  # Redirect to the admin dashboard after updating

    return render(request, 'update_leave_status.html', {'leave_application': leave_application})

@admin_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'list_employee.html', {'employees': employees})

@admin_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    
    return render(request, 'employee_form.html', {'form': form})

@admin_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employee_form.html', {'form': form})

@admin_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')
    
    return render(request, 'employee_confirm_delete.html', {'employee': employee})

@login_required
def history(request):
    # Filter leave applications for the logged-in employee
    leave_applications = LeaveApl.objects.filter(empid=request.user.employee)
    context = {
        "leave_applications": [application.extract() for application in leave_applications],
        'leave_types': leave_types,
        'leave_statuses': leave_statuses,
    }
    
    return render(request, "history.html", context)