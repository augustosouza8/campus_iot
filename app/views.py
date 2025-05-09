"""
Route handlers for the Campus IoT Management System.

HELLO
"""

from urllib.parse import urlparse
from app.analysis import (summarize_sensors, summarize_feedback, simulate_live_temperatures,
                          suggest_thermostat_adjustments, aggregate_sensor_features,
                          get_demo_outdoor_data)

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request, abort
)
from flask_login import (
    login_user, logout_user,
    current_user, login_required
)

from app import db
from app.models import User, Sensor, Calibration, Feedback, TemperatureReading
from app.forms import (
    LoginForm, SensorForm,
    CalibrationForm, FeedbackForm,
    ActionForm
)

bp = Blueprint('main', __name__)


@bp.route('/', endpoint='home')
def home():
    return render_template('home.html', title='Home')


@bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login_view():
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
    logout_user()
    return redirect(url_for('main.home'))


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

@bp.route('/sensors/toggle_status', methods=['POST'], endpoint='toggle_sensor_status')
@login_required
def toggle_sensor_status():
    if current_user.role != 'admin':
        abort(403)
    form = ActionForm()
    if form.validate_on_submit():
        sensor = db.session.get(Sensor, int(form.record_id.data))
        if sensor:
            sensor.status = 'offline' if sensor.status == 'online' else 'online'
            sensor.set_status(new_status=sensor.status)
            db.session.commit()
            flash(f'Sensor status changed to {sensor.status}.', 'info')
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


@bp.route('/student', methods=['GET'], endpoint='student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        abort(403)
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


@bp.route('/admin', methods=['GET'], endpoint='admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)

    # Fetch data
    sensors   = db.session.scalars(db.select(Sensor)).all()
    feedbacks = db.session.scalars(db.select(Feedback)).all()

    # Generate AI-style summaries
    sensor_summary   = summarize_sensors(sensors)
    feedback_summary = summarize_feedback(feedbacks)

    # Compute sensor counts
    all_sensors   = sensors
    online_count  = sum(1 for s in sensors if s.status == 'online')
    offline_count = sum(1 for s in sensors if s.status == 'offline')

    # Compute overall feedback counts
    all_feedbacks = feedbacks
    hot_count     = sum(1 for fb in feedbacks if fb.rating == 'hot')
    ok_count      = sum(1 for fb in feedbacks if fb.rating == 'ok')
    cold_count    = sum(1 for fb in feedbacks if fb.rating == 'cold')

    # Compute per-sensor feedback counts for table badges
    feedback_counts = { s.id: {'hot':0, 'ok':0, 'cold':0} for s in sensors }
    for fb in feedbacks:
        if fb.sensor_id in feedback_counts:
            feedback_counts[fb.sensor_id][fb.rating] += 1

    # Simulate live temperature per sensor
    live_temps = simulate_live_temperatures(sensors)

    # Use hard‑coded outdoor data
    outdoor_data = get_demo_outdoor_data()
    latest_outdoor_temp = outdoor_data[-1].temp if outdoor_data else None

    # Generate thermostat adjustment suggestions
    thermostat_suggestions = suggest_thermostat_adjustments(
        sensors,
        feedbacks,
        live_temps
    )

    # Load historical temperature readings (last 2 hours)
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(hours=2)
    rows = db.session.scalars(
        db.select(TemperatureReading)
          .where(TemperatureReading.timestamp >= cutoff)
    ).all()
    historical_temps = {}
    for tr in rows:
        historical_temps.setdefault(tr.sensor_id, []).append((tr.timestamp, tr.temperature))

    # Build feature vectors for ML/demo
    feature_vectors = aggregate_sensor_features(
        sensors=sensors,
        feedbacks=feedbacks,
        live_temps=live_temps,
        historical_temps=historical_temps,
        outdoor_data=outdoor_data
    )
    from app.analysis import ACCEPTABLE_LOW, ACCEPTABLE_HIGH
    return render_template(
        'admin_dashboard.html',
        title='Admin Dashboard',
        all_sensors=all_sensors,
        online_count=online_count,
        offline_count=offline_count,
        all_feedbacks=all_feedbacks,
        hot_count=hot_count,
        ok_count=ok_count,
        cold_count=cold_count,
        feedback_counts=feedback_counts,
        sensor_summary=sensor_summary,
        feedback_summary=feedback_summary,
        live_temps=live_temps,
        thermostat_suggestions=thermostat_suggestions,
        feature_vectors=feature_vectors,
        outdoor_data=outdoor_data,
        latest_outdoor_temp=latest_outdoor_temp,
        # thresholds for template coloring
        ACCEPTABLE_LOW=ACCEPTABLE_LOW,
        ACCEPTABLE_HIGH=ACCEPTABLE_HIGH,
    )

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


# View to show all feedbacks (admin only)
@bp.route('/feedbacks', methods=['GET'], endpoint='all_feedbacks')
@login_required
def all_feedbacks():
    if current_user.role != 'admin':
        abort(403)
    # Fetch all feedback entries
    feedbacks = db.session.scalars(db.select(Feedback)).all()
    return render_template(
        'all_feedbacks.html',
        title='All Feedbacks',
        feedbacks=feedbacks
    )
