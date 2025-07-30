LEA Disciplinary Management System
An efficient, role-based system for tracking member attendance and monitoring compliance within an organization. The application features distinct dashboards and privileges for regular Members, Committee members, and Leadership (Admins).
Core Features
Role-Based Access Control: Three user roles (Member, Committee, Admin) with distinct permissions and views.
Member Dashboard: Personalized view for members to mark attendance, view their compliance status, and see their attendance trends on a chart.
Admin Dashboard: A comprehensive overview of the entire organization, including total members, overall compliance rate, and daily attendance statistics.
Custom Member Management: Admins can view a list of all members, click into a detailed profile for each member, and see their individual statistics and attendance trends.
Attendance Tracking: A simple form for members to mark their attendance for different session types (Physical, Online, Meetup).
Profile Management: Users can update their personal information and upload a profile picture.
Dark Theme UI: A sleek, modern dark-mode user interface built with Tailwind CSS and Alpine.js.
Tech Stack
Backend: Python, Django
Database: SQLite3 (for development)
Frontend: HTML, Tailwind CSS
JavaScript: Alpine.js (for UI interactivity), Chart.js (for data visualization)
Dependencies: Node.js/npm (for Tailwind CSS)
Prerequisites
Before you begin, ensure you have the following installed on your local machine:
Python 3.10+
Node.js and npm
Git
Setup Instructions
Follow these steps to get your local development environment running.
1. Clone the Repository
Generated bash
git clone <repository-url>
cd lea_disciplinary_system
Use code with caution.
Bash
2. Set Up the Python Environment
It is highly recommended to use a virtual environment to manage project dependencies.
Generated bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Use code with caution.
Bash
3. Install Backend Dependencies
Install all required Python packages using the requirements.txt file.
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
(This will install Django, Pillow, and any other necessary packages.)
4. Install Frontend Dependencies
This project uses Tailwind CSS, which requires Node.js dependencies.
Generated bash
# This will install Tailwind CSS and any other dev dependencies
npm install
Use code with caution.
Bash
5. Initialize the Database
Run the initial Django migrations to create the database schema.
Generated bash
python manage.py migrate
Use code with caution.
Bash
6. Create a Superuser
You need an initial admin account to log in and manage the system.
Generated bash
python manage.py createsuperuser
Use code with caution.
Bash
Follow the prompts to create a username, email, and password.
Running the Application
To run the full application in development, you will need to have two terminals open and running simultaneously.
Terminal 1: Run the Django Development Server
This terminal will run the Python backend.
Generated bash
# Make sure your virtual environment is activated
python manage.py runserver
Use code with caution.
Bash
The Django application will be available at http://127.0.0.1:8000/.
Terminal 2: Run the Tailwind CSS Build Process
This terminal will watch your template files for any changes to CSS classes and automatically rebuild your stylesheet.
Generated bash
# This command watches for changes and rebuilds output.css
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
Use code with caution.
Bash
You must keep this terminal running while you are making any changes to the HTML files to ensure your styles are up-to-date.
IMPORTANT: First-Time Admin Setup
After creating your superuser, you must assign the correct role to it to access the custom admin dashboard and features.
Start both servers as described above.
Navigate to the default Django admin panel: http://127.0.0.1:8000/admin/.
Log in with the superuser credentials you created.
On the admin homepage, click on "Users".
Find and click on the username of the superuser you just created.
Scroll down to the "Role" field.
Change the role from "Member" to "Admin".
Click "Save" at the bottom of the page.
Now, you can log out of the /admin panel and log in through the main site's login page. You will be correctly redirected to the custom Admin Dashboard and have access to all administrative features.
Project Structure Overview
/config/core/: Contains project-level settings (settings.py) and URL configuration (urls.py).
/lea_app/: The main application containing models, views, forms, and app-specific URLs.
/templates/: Contains all HTML templates for the project.
/templates/admin/: Templates for the custom admin views.
/templates/user/: Templates for the standard member views.
/templates/partials/: Reusable template components like the navbar.
/static/: Contains all static assets.
/static/css/input.css: The source file for Tailwind CSS.
/static/css/output.css: The generated stylesheet. Do not edit this file directly.
/static/images/: For project images like the default avatar.
/media/: This directory will be created automatically when the first file (e.g., a profile picture) is uploaded. It is ignored by Git.
