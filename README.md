# **Campus IoT Management System**

## **Overview**

Campus IoT is a Flask-based web application for combating energy wastage on campus through smart setting of heating systems based on  IoT sensor data and human input. Students can submit temperature feedback, and administrators can add, remove, and calibrate sensors, as well as view analytics based on sensor status and feedback. Data is collected and aggregated in a dataclass containing vectors that would be outputted to an AI/ML system which tailors suggestions to decrease heating waste. Current implementation of this feature is simplistic but core functionality and interfaces are established.

## **Contributions**
- Augusto Souza - 20% - Database, classes, forms
- Frederick Dobbin - 20% - Demo video, design principles, plan test cases & core features
- Algot Norlin - 20% - Sensors, feedback, models
- Harry Sadleir - 20% - Admin dashboard, AI/ML, setup instructions (github: woofdog7777)
- Harry Thomas - 20% - Observers, implement test cases, readme


## **Features**

- **User Authentication**: Secure login for admins and students using Flask-Login.

- **Sensor Management** (Admin-only): Create, view, remove, and calibrate sensors.

- **Student Feedback**: Students submit temperature ratings (`hot`, `ok`, `cold`) with optional comments.

- **Admin Dashboard**: Summaries of sensor statuses and feedback distributions, simple sensor-data and feedback based suggestions (AI/ML interface built and ready for integration).

- **Database Seeding**: `reset_db()` utility to drop, recreate, and seed the database with sample data for development.

- **Testing**: Testcases can be found withing the 'tests' directory.

## **Design & Architecture**
- **Languages Used**: Python, HTML, CSS

- **Application Factory Pattern**: Central `create_app()` in `app/__init__.py` for flexible configuration and testing.

- **Blueprints**: Routes organized in a `main` blueprint (`app/views.py`).

- **MVC Structure**: Models (`app/models.py`), Views (`app/views.py`), Templates (`app/templates/`).

- **Design Principles**:

  - **Single Responsibility**: Forms, models, and view logic are decoupled into separate modules.

  - **Dependency Injection**: Flask extensions (`db`, `login`) initialized in the factory function.

- **Design Pattern**:

  - Observer design pattern added to notify the dashboard of the sensor status changes.

- **Class Relationships**:

  - Association: One-to-many between Users ↔ Feedbacks, Sensors ↔ Calibrations, Sensors ↔ Feedbacks.

  - Inheritance: `User` inherits from Flask-Login’s `UserMixin`; models inherit from `db.Model`.


## **Getting Started**

Login details:

Student Username: student1
Admin Username: admin1

All passwords: password123

Database is included for ease of testing.

# Project Setup Guide

This guide walks you through setting up the project using a Python virtual environment.

---
## 1. Clone the repository


git clone git@github.com:augustosouza8/campus_iot.git
cd campus_iot

⸻
2. Create a virtual environment

python3 -m venv venv

⸻
3. Activate the virtual environment

macOS/Linux:

source venv/bin/activate

Windows (CMD):

venv\Scripts\activate

Windows (PowerShell):

.\venv\Scripts\Activate.ps1
⸻

4. Install dependencies

pip install -r requirements.txt



⸻

5. (Optional - If using PyCharm GUI) Set interpreter in PyCharm
	1.	Open the project in PyCharm.
	2.	Go to Settings > Project > Python Interpreter
	3.	Click the gear icon (⚙️) → Add…
	4.	Choose “Existing environment”
	5.	Select:
	•	venv/bin/python (on macOS/Linux)
	•	venv\Scripts\python.exe (on Windows)

PyCharm will now use your virtual environment.

6. Open Project in pycharm, go to Run > Edit configurations > Python > set module to 'flask' > set script parameters to 'run'


### **Running the Application**

From project root:
1) Activate your virtualenv

source venv/bin/activate
2) Rename .flaskenv.example to .flaskenv or create a new .flaskenv with the following text:

FLASK_APP=run.py

FLASK_ENV=development

FLASK_DEBUG=1

FLASK_RUN_PORT=5001

Open your browser to `http://localhost:5001`.





## **Future Work**

- Implement real analytics based on vectors gathered (visible on the admin dashboard).

- Integrate with external sensor APIs using the Adapter pattern.

- Migrate to PostgreSQL or another production-grade database.

- Enhance UI/UX with a more polished Bootstrap theme and client-side validation, accessibility features.
