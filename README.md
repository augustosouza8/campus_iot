# **Campus IoT Management System**

## **Overview**

Campus IoT is a Flask-based web application for managing and monitoring IoT sensors across campus rooms. Students can submit temperature feedback, and administrators can add, remove, and calibrate sensors, as well as view analytics based on sensor status and feedback.


## **Features**

- **User Authentication**: Secure login for admins and students using Flask-Login.

- **Sensor Management** (Admin-only): Create, view, remove, and calibrate sensors.

- **Student Feedback**: Students submit temperature ratings (`hot`, `ok`, `cold`) with optional comments.

- **Admin Dashboard**: Dummy AI summaries of sensor statuses and feedback distributions.

- **Database Seeding**: `reset_db()` utility to drop, recreate, and seed the database with sample data for development.


## **Design & Architecture**

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

### **Prerequisites**

- Python 3.8 or higher

- `virtualenv` (recommended)


### **Installation**

git clone https\://github.com/augustosouza8/campus\_iot.git

cd campus\_iot

python -m venv venv

source venv/bin/activate  # On Windows: venv\\\Scripts\\\activate

pip install -r requirements.txt


### **Configuration**

Copy `.flaskenv.example` to `.flaskenv`

1. Open flask shell
2. Run 'reset_db()'
3. By default, the app uses SQLite at `app/data/data.sqlite`. To change the database, update `SQLALCHEMY_DATABASE_URI` in `config.py`.

### **Running the Application**

From project root:
1) Activate your virtualenv

source venv/bin/activate
2) Export Flask env vars (so Flask knows what to run and that you want debug mode)

export FLASK_APP=run.py

export FLASK_ENV=development

3) Start the server on port 5001

flask run --port=5001


Open your browser to `http://localhost:5001`.


## **Testing**

_(To be added)_

We aim to include unit and integration tests using `pytest` and Flask’s test client. Example setup:

pip install pytest pytest-flask

pytest


## **Future Work**

- Implement real analytics and interactive charts in the admin dashboard.

- Integrate with external sensor APIs using the Adapter pattern.

- Add comprehensive unit and negative test cases for each feature.

- Migrate to PostgreSQL or another production-grade database.

- Enhance UI/UX with a more polished Bootstrap theme and client-side validation.


## **License**

This project is licensed under the MIT License. See the[ LICENSE](https://chatgpt.com/c/LICENSE) file for details..
