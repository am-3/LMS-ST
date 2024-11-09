from django import forms
from LMSApp import models

#required_field=False
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ['empid', 'name', 'email']

    def clean_empid(self):
        empid = self.cleaned_data.get('empid')
        if self.instance.pk:  # If it's an update
            # Check for other existing employees with the same empid
            if models.Employee.objects.exclude(pk=self.instance.pk).filter(empid=empid).exists():
                raise forms.ValidationError("An employee with this ID already exists.")
        return empid

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveAplForm(forms.ModelForm):
    class Meta:
        model = models.LeaveApl
        fields = ['empid', 'leaveDate', 'returnDate', 'reason']  

    def __init__(self, *args, **kwargs):
        super(LeaveAplForm, self).__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs.update({'class': 'form-control'})

        # Make empid a read-only field
        self.fields['empid'].widget.attrs['readonly'] = 'readonly'
        self.fields['empid'].widget.attrs['class'] = 'form-control'

        # Set the widget for date fields to DateInput
        self.fields['leaveDate'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['returnDate'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        leave_date = cleaned_data.get("leaveDate")
        return_date = cleaned_data.get("returnDate")

        if leave_date and return_date:
            if return_date <= leave_date:
                raise forms.ValidationError("Return date must be after the leave date.")

        return cleaned_data