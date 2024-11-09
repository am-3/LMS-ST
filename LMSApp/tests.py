from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Employee

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
