from django.db import models
from django.contrib.auth.models import User  # Import the User model
from django.core.exceptions import ValidationError

def generate_empid():
    try:
        highest_empid = Employee.objects.aggregate(max_empid=models.Max('empid'))['max_empid']
        return (highest_empid + 1) if highest_empid is not None else 1
    except Exception as e:
        print(f"Error generating empid: {e}")
        raise ValidationError("Could not generate empid.")

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Add this line
    empid = models.IntegerField(unique=True) #max_length=8)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=150)

    def __str__(self) -> str:
        return str(self.empid)

class LeaveApl(models.Model):
    aplid = models.AutoField(primary_key=True)
    empid = models.ForeignKey(Employee, on_delete=models.CASCADE)
    apl_date = models.DateField(auto_now_add=True)
    leaveDate = models.DateField()
    returnDate = models.DateField() #Return to office date
    reason = models.CharField(choices=[('PER', 'Personal Leave'), ('OFI', 'Official Work'), ('PTO', 'Paid Time Off'), ('EMR', 'Emergency')], max_length=3)
    status = models.CharField(choices=[('SUB', 'Submitted'), ('ACP', 'Accepted'), ('REJ', 'Rejected'), ('DEF', 'Deffered')], max_length=3, default='SUB')

    #Function for filtering data
    def extract(self):
        row = [
            self.aplid,
            self.empid,
            self.apl_date,
            self.leaveDate,
            self.returnDate,
            self.reason,
            self.status
        ]
        return row

