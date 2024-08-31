# PersonalFinance

Personal Finance System is a Flask-based web application that allows users to securely manage and pay loans online. This project integrates user authentication, balance management, and payment processing to provide a seamless and efficient experience for users to handle their financial obligations.

Features
User Authentication: Secure login and logout functionality to ensure only authorized users can access their accounts.
Balance Management: Users can view their total balance and make payments towards their house bills.
Bill Payment: Users can easily pay their house bills through the system. The system checks for sufficient funds and updates the balance and bill status accordingly.
Error Handling: Comprehensive error handling for invalid inputs, insufficient funds, and transaction failures.
Responsive Design: A user-friendly interface that adapts to different screen sizes, ensuring accessibility on both desktop and mobile devices.

Technology Stack
Backend: Python, Flask
Frontend: HTML, CSS
Database: SQLAlchemy (SQLite/PostgreSQL/MySQL)
Authentication: Flask-Login
Installation
Prerequisites
Python 3.x
Pip (Python package installer)



Usage
Sign Up: Create an account to get started.
Login: Access your account using your credentials.
Check Balance: View your total balance and outstanding house bills.
Pay Bills: Enter the amount and submit to pay your house bills.
Logout: Securely log out of your account when done.


Project stracture
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── pay-house-bills.html
│   │   └── ...
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── ...
├── migrations/
├── venv/
├── .env
├── requirements.txt
├── config.py
└── README.md



Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any inquiries or issues, please reach out to [i22.shahinyan.armen.aris@etud.ufar.am].


