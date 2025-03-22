# School Management System

## Description
The **School Management System** is a robust platform designed to streamline classroom, teacher, and student management while facilitating real-time communication and enhancing administrative efficiency. 
It features dynamic dashboards, role-based access control, and tools for managing academic records, exam results, and leave requests—all in a user-friendly interface tailored for educational institutions.

## Key Features
- **Classroom and Teacher Management**: Efficient handling of classroom assignments and teacher responsibilities.
- **Role-Based Access Control**: Secure authentication and authorization using **JWT**, tailored for Admin, Staff, and Students.
- **Real-Time Communication**: Integrated chat and notification system powered by **Django Channels** and **WebSockets** for seamless collaboration.
- **Exam and Results System**: Intelligent tools to track grades and monitor academic performance.
- **Dynamic Dashboards**: Real-time insights into key metrics for administrators, staff, and students.
- **Responsive User Interface**: Modern design with **Tailwind CSS**, ensuring a smooth experience across devices.

## Technologies Used
### Backend
- **Django**: For building scalable APIs.
- **Django REST Framework (DRF)**: For efficient API development.
- **Django Channels**: For real-time chat and notifications.
- **PostgreSQL**: Robust and scalable data storage.
- **JWT (JSON Web Tokens)**: Secure authentication.

### Frontend
- **ReactJS**: For a dynamic and interactive user interface.
- **Redux**: For efficient state management.
- **Tailwind CSS**: For responsive and modern UI design.

### Deployment
- **Backend**: Deployed on **AWS EC2** with **Nginx** and **Daphne** for performance and scalability.
- **Frontend**: Deployed on **Vercel** for high availability and security.

## Installation

### Prerequisites
- Python 3.9+
- Node.js 14+
- PostgreSQL
- Virtual Environment Manager (e.g., `venv`)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ayshashfi/School-BACKEND.git
   cd School-BACKEND

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Configure the database:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver

### Frontend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ayshashfi/School-FRONTEND.git
   cd School-FRONTEND

2. Navigate to the frontend folder:
   cd School-FRONTEND

3. Install dependencies:
   npm install

4. Start the development server:
   npm start

Usage
Access the application at http://127.0.0.1:8000 for the backend and http://localhost:3000 for the frontend.

Deployment
The system is deployed as follows:

Backend: Hosted on AWS EC2 with Nginx and Daphne.
Frontend: Hosted on Vercel for fast and secure delivery.







