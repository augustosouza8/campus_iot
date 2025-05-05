"""
Route handlers for the Campus IoT Management System.
"""

from urllib.parse import urlparse

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request, abort
)
from flask_login import (
    login_user, logout_user,
    current_user, login_required
)

from app import db
from app.models import User, Sensor, Calibration, Feedback
from app.forms import (
    LoginForm, SensorForm,
    CalibrationForm, FeedbackForm,
    ActionForm
)

# Define a blueprint named “main”
bp = Blueprint('main', __name__)


@bp.route('/', endpoint='home')
def home():
    """Public home page."""
    return render_template('home.html', title='Home')


@bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login_view():
    """
    Handle login for both admins and students.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)

    return render_template('generic_form.html', title='Sign In', form=form)


@bp.route('/logout', endpoint='logout')
def logout_view():
    """Log out the current user."""
    logout_user()
    return redirect(url_for('main.home'))


# -- Admin‐only sensor management --------------------------------------------

@bp.route('/sensors', methods=['GET', 'POST'], endpoint='sensors')
@login_required
def sensors():
    if current_user.role != 'admin':
        abort(403)

    sensor_form = SensorForm()
    action_form = ActionForm()

    if sensor_form.validate_on_submit():
        new_sensor = Sensor(
            name=sensor_form.name.data,
            location=sensor_form.location.data,
            status=sensor_form.status.data
        )
        db.session.add(new_sensor)
        db.session.commit()
        flash('Sensor added successfully.', 'success')
        return redirect(url_for('main.sensors'))

    all_sensors = db.session.scalars(db.select(Sensor)).all()
    return render_template(
        'sensor_list.html',
        title='Sensors',
        sensors=all_sensors,
        sensor_form=sensor_form,
        action_form=action_form
    )


@bp.route('/sensors/<int:id>', methods=['GET'], endpoint='sensor_detail')
@login_required
def sensor_detail(id):
    if current_user.role != 'admin':
        abort(403)

    sensor = db.session.get(Sensor, id)
    if sensor is None:
        return redirect(url_for('main.sensors'))

    calibration_form = CalibrationForm()
    calibration_form.sensor_id.data = sensor.id

    return render_template(
        'sensor_detail.html',
        title=f'Sensor {sensor.name}',
        sensor=sensor,
        calibration_form=calibration_form
    )


@bp.route('/sensors/remove', methods=['POST'], endpoint='remove_sensor')
@login_required
def remove_sensor():
    if current_user.role != 'admin':
        abort(403)

    form = ActionForm()
    if form.validate_on_submit():
        sensor = db.session.get(Sensor, int(form.record_id.data))
        if sensor:
            db.session.delete(sensor)
            db.session.commit()
            flash('Sensor removed.', 'warning')
    return redirect(url_for('main.sensors'))


@bp.route('/sensors/calibrate', methods=['POST'], endpoint='calibrate_sensor')
@login_required
def calibrate_sensor():
    if current_user.role != 'admin':
        abort(403)

    form = CalibrationForm()
    if form.validate_on_submit():
        cal = Calibration(
            sensor_id=int(form.sensor_id.data),
            notes=form.notes.data
        )
        db.session.add(cal)
        db.session.commit()
        flash('Calibration recorded.', 'info')
    return redirect(url_for('main.sensor_detail', id=form.sensor_id.data))


# -- Student feedback -------------------------------------------------------

@bp.route('/student', methods=['GET'], endpoint='student_dashboard')
@login_required
def student_dashboard():
    """
    Landing page for students.
    Instantiates and passes feedback_form to the template so it never is undefined.
    """
    if current_user.role != 'student':
        abort(403)

    # Create the form and populate sensor choices
    form = FeedbackForm()
    form.sensor_id.choices = [
        (s.id, f"{s.name} ({s.location})")
        for s in db.session.scalars(db.select(Sensor)).all()
    ]

    return render_template(
        'student_feedback.html',
        title='Feedback',
        feedback_form=form
    )


@bp.route('/feedback', methods=['GET', 'POST'], endpoint='submit_feedback')
@login_required
def submit_feedback():
    """
    Show feedback form (GET) and process it (POST).
    """
    if current_user.role != 'student':
        abort(403)

    form = FeedbackForm()
    form.sensor_id.choices = [
        (s.id, f"{s.name} ({s.location})")
        for s in db.session.scalars(db.select(Sensor)).all()
    ]

    if form.validate_on_submit():
        fb = Feedback(
            user_id=current_user.id,
            sensor_id=form.sensor_id.data,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(fb)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.student_dashboard'))

    return render_template(
        'student_feedback.html',
        title='Submit Feedback',
        feedback_form=form
    )


# -- Admin analytics --------------------------------------------------------

@bp.route('/admin', methods=['GET'], endpoint='admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)

    sensors = db.session.scalars(db.select(Sensor)).all()
    feedbacks = db.session.scalars(db.select(Feedback)).all()

    sensor_summary = (
        f"Total sensors: {len(sensors)}; "
        f"Online: {sum(s.status=='online' for s in sensors)}; "
        f"Offline: {sum(s.status=='offline' for s in sensors)}"
    )
    feedback_summary = (
        f"Total feedbacks: {len(feedbacks)}; "
        f"Hot: {sum(fb.rating=='hot' for fb in feedbacks)}; "
        f"OK: {sum(fb.rating=='ok' for fb in feedbacks)}; "
        f"Cold: {sum(fb.rating=='cold' for fb in feedbacks)}"
    )

    return render_template(
        'admin_dashboard.html',
        title='Admin Dashboard',
        sensor_summary=sensor_summary,
        feedback_summary=feedback_summary
    )


# -- Error handlers ---------------------------------------------------------

@bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403


@bp.app_errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', title='Not Found'), 404


@bp.app_errorhandler(413)
def too_large(error):
    return render_template('errors/413.html', title='Request Too Large'), 413


@bp.app_errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500
