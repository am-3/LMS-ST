from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Employee, LeaveApl
from .forms import LeaveAplForm

class EmployeeCRUDTest(TestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        
        # Create a non-admin user for access restriction tests
        self.non_admin_user = User.objects.create_user(username='user', email='user@example.com', password='userpass')

        # Log in as the admin user
        self.client.login(username='admin', password='adminpass')

        # Create an initial employee for testing update and delete functionality
        self.employee = Employee.objects.create(empid=1001, name='John Doe', email='john@example.com')

    def test_employee_list_view_as_admin(self):
        # Test that the admin can access the employee list view
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_employee.html')
        self.assertContains(response, 'John Doe')  # Ensure employee is in the response

    def test_employee_create_view_as_admin(self):
        # Test that the admin can create a new employee
        response = self.client.post(reverse('employee_create'), {
            'empid': 1002,
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertTrue(Employee.objects.filter(empid=1002).exists())

    def test_employee_update_view_as_admin(self):
        # Test that the admin can update an employee
        response = self.client.post(reverse('employee_update', args=[self.employee.pk]), {
            'empid': 1001,  # Keep the same empid
            'name': 'John Updated',
            'email': 'john_updated@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'John Updated')  # Check that the name was updated

    def test_employee_delete_view_as_admin(self):
        # Test that the admin can delete an employee
        response = self.client.post(reverse('employee_delete', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful delete
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_employee_create_view_as_non_admin(self):
        # Log in as a non-admin user
        self.client.logout()
        self.client.login(username='user', password='userpass')

        # Non-admin should not be able to access the create employee view
        response = self.client.get(reverse('employee_create'))
        self.assertEqual(response.status_code, 403)  # Should now get forbidden access


    def test_employee_update_view_as_non_admin(self):
        # Log in as a non-admin user
        self.client.logout()
        self.client.login(username='user', password='userpass')

        # Non-admin should not be able to access the update employee view
        response = self.client.get(reverse('employee_update', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 403)  # Access should be forbidden

    def test_employee_delete_view_as_non_admin(self):
        # Log in as a non-admin user
        self.client.logout()
        self.client.login(username='user', password='userpass')

        # Non-admin should not be able to access the delete employee view
        response = self.client.get(reverse('employee_delete', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 403)  # Access should be forbidden


class ExtendedEmployeeCRUDTest(TestCase):

    def setUp(self):
        # Existing setup with admin and non-admin users, and an initial employee
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.non_admin_user = User.objects.create_user(username='user', email='user@example.com', password='userpass')
        self.client.login(username='admin', password='adminpass')
        self.employee = Employee.objects.create(empid=1001, name='John Doe', email='john@example.com')
        
        # Set up a leave application for testing
        self.leave = LeaveApl.objects.create(
            empid=self.employee,
            leave_type='PTO',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            status='SUB',
        )

    def test_employee_list_view_as_non_admin(self):
        # Ensure non-admin users cannot access employee list view
        self.client.logout()
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 403)

    def test_leave_application_submission(self):
        # Test that an employee can submit a leave application
        self.client.logout()
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('apply'), {
            'leave_type': 'PTO',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=2)
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(LeaveApl.objects.filter(empid=self.non_admin_user.employee).exists())

    def test_leave_application_update_status_as_admin(self):
        # Ensure admin can update the status of a leave application
        response = self.client.post(reverse('update_leave_status', args=[self.leave.aplid]), {
            'status': 'ACP'
        })
        self.assertEqual(response.status_code, 302)
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, 'ACP')  # Status should be updated to 'Accepted'

    def test_invalid_employee_creation(self):
        # Test for invalid data handling in employee creation
        response = self.client.post(reverse('employee_create'), {
            'empid': '',  # Invalid data (empty empid)
            'name': 'Invalid Employee',
            'email': 'invalid@example.com'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page with form errors
        self.assertContains(response, "This field is required.")  # Check for validation error

    def test_apply_leave_form_validation(self):
        # Validate form handling for leave application
        form = LeaveAplForm(data={
            'leave_type': 'PTO',
            'start_date': date.today(),
            'end_date': date.today() - timedelta(days=1)  # End date before start date
        })
        self.assertFalse(form.is_valid())  # Form should be invalid due to end_date < start_date
        self.assertIn('end_date', form.errors)

    def test_dashboard_view(self):
        # Test dashboard view for logged-in user
        self.client.logout()
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emp_dashboard.html')
        self.assertContains(response, 'pending_leaves')  # Check context variable availability

    def test_admin_dashboard_view(self):
        # Ensure admin can access the admin dashboard
        response = self.client.get(reverse('admindashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')
        self.assertContains(response, 'leave_applications')  # Check context variable availability
