# Leave Management System

A streamlined web application for managing employee leaves. This system provides employees with a dashboard to view leave counts, a form to apply for leave, and gives admins the tools to manage leave requests efficiently.

## Features

- **Employee Dashboard**: Displays the types of leaves available and their respective counts.
- **Leave Application Form**: Allows employees to submit leave applications directly from the dashboard.
- **Admin Page**: Empowers the admin to view, approve, or reject employee leave applications.
- **Leave History**: A detailed view of the leave history for each employee.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Virendra69/Leave-Management-System.git
2. Navigate into the project directory:
   ```bash
   cd Leave-Management-System
3. Install dependencies (if using Node.js, Python, or other specific environments):
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
   python manage.py runserver

## Usage

1. **Employee Access**:
   - Employees can log in to view their **Dashboard**, which displays leave types and remaining counts.
   - To request leave, fill out the **Leave Application Form** with details such as the dates, type of leave, and reason.
   - Track the status of past leave requests through the **Leave History** section.

2. **Admin Access**:
   - The Admin can review all submitted leave requests in the **Admin Page**.
   - For each request, the Admin has options to **Approve** or **Reject** based on company policies.
   - Leave approvals and rejections will be updated in the **Leave History** section for employees to view.

3. **Leave History**:
   - Both employees and admins can access the **Leave History** to view past requests, statuses, and details.

## Contributing
Feel free to contribute by submitting a pull request. Make sure to follow the existing code style and add necessary documentation for any new features.

## License
This project is licensed under the MIT License.
