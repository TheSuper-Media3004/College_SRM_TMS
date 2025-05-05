from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Bus, Route, Student, BoardingPoint, Complaint
from sqlalchemy import text
from datetime import datetime, time
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '80897097087098798'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_tms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create tables within app context
with app.app_context():
    db.create_all()


def init_db_from_schema():
    with app.app_context():
        with open('schema.sql', 'r') as f:
            sql_commands = f.read()


        commands = sql_commands.split(';')

        with db.engine.connect() as conn:
            for command in commands:
                if command.strip():
                    conn.execute(text(command))
            conn.commit()

        print("Database schema created successfully!")


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Dashboard route
@app.route('/')
@login_required
def index():
    buses_count = Bus.query.count()
    routes_count = Route.query.count()
    students_count = Student.query.count()
    return render_template('index.html',
                           buses_count=buses_count,
                           routes_count=routes_count,
                           students_count=students_count)


# Bus routes
@app.route('/buses', methods=['GET', 'POST'])
@login_required
def buses():
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        driver_name = request.form['driver_name']

        # Validate input
        if not bus_number or not driver_name:
            flash('Please fill all fields!', 'error')
            return redirect(url_for('buses'))

        # Check if bus number already exists
        existing_bus = Bus.query.filter_by(bus_number=bus_number).first()
        if existing_bus:
            flash(f'Bus number {bus_number} already exists!', 'error')
            return redirect(url_for('buses'))

        new_bus = Bus(bus_number=bus_number, driver_name=driver_name)
        db.session.add(new_bus)

        try:
            db.session.commit()
            flash('Bus added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding bus: {str(e)}', 'error')

        return redirect(url_for('buses'))

    buses = Bus.query.all()
    return render_template('buses.html', buses=buses)


@app.route('/buses/delete/<int:id>', methods=['POST'])
@login_required
def delete_bus(id):
    bus = Bus.query.get_or_404(id)

    try:
        db.session.delete(bus)
        db.session.commit()
        flash('Bus deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bus: {str(e)}', 'error')

    return redirect(url_for('buses'))


# Routes management
@app.route('/routes', methods=['GET', 'POST'])
@login_required
def routes():
    if request.method == 'POST':
        route_number = request.form['route_number']
        route_name = request.form['route_name']

        # Validate input
        if not route_number or not route_name:
            flash('Please fill all fields!', 'error')
            return redirect(url_for('routes'))

        new_route = Route(route_number=route_number, route_name=route_name)
        db.session.add(new_route)

        try:
            db.session.commit()
            flash('Route added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding route: {str(e)}', 'error')

        return redirect(url_for('routes'))

    routes = Route.query.all()
    return render_template('routes.html', routes=routes)


@app.route('/routes/delete/<int:id>', methods=['POST'])
@login_required
def delete_route(id):
    route = Route.query.get_or_404(id)

    try:
        db.session.delete(route)
        db.session.commit()
        flash('Route deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting route: {str(e)}', 'error')

    return redirect(url_for('routes'))


# Boarding points management
@app.route('/boarding-points/<int:route_id>', methods=['GET', 'POST'])
@login_required
def boarding_points(route_id):
    route = Route.query.get_or_404(route_id)

    if request.method == 'POST':
        stop_number = request.form['stop_number']
        location = request.form['location']
        pickup_hour = int(request.form['pickup_hour'])
        pickup_minute = int(request.form['pickup_minute'])

        # Validate input
        if not stop_number or not location:
            flash('Please fill all fields!', 'error')
            return redirect(url_for('boarding_points', route_id=route_id))

        pickup_time = time(pickup_hour, pickup_minute)
        new_point = BoardingPoint(
            stop_number=stop_number,
            location=location,
            pickup_time=pickup_time,
            route_id=route_id
        )
        db.session.add(new_point)

        try:
            db.session.commit()
            flash('Boarding point added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding boarding point: {str(e)}', 'error')

        return redirect(url_for('boarding_points', route_id=route_id))

    boarding_points = BoardingPoint.query.filter_by(route_id=route_id).order_by(BoardingPoint.stop_number).all()
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBouqkJ2-hlZDXlmmuPhxDKuuqtontg_hM')
    genai.configure(api_key=GEMINI_API_KEY)
    travel_times = []
    locations = [point.location for point in boarding_points]
    if len(locations) > 1:
        prompt = "Estimate the travel time in minutes between each consecutive pair of these locations in Chennai, India, considering typical morning traffic. Return a comma-separated list of durations in minutes, in order. Locations: " + ", ".join(locations)
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            import re
            times = re.findall(r'\d+', response.text)
            for t in times:
                travel_times.append(f"{t} min")
            while len(travel_times) < len(locations) - 1:
                travel_times.append('N/A')
        except Exception as e:
            travel_times = ['N/A'] * (len(locations) - 1)
    else:
        travel_times = ['N/A'] * (len(locations) - 1)
    travel_times.append('N/A')

    return render_template('boarding_points.html', route=route, boarding_points=boarding_points, travel_times=travel_times)


@app.route('/boarding-points/delete/<int:id>', methods=['POST'])
@login_required
def delete_boarding_point(id):
    point = BoardingPoint.query.get_or_404(id)
    route_id = point.route_id

    try:
        db.session.delete(point)
        db.session.commit()
        flash('Boarding point deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting boarding point: {str(e)}', 'error')

    return redirect(url_for('boarding_points', route_id=route_id))


# Students management
@app.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    if request.method == 'POST':
        student_name = request.form['student_name']
        enrollment_number = request.form['enrollment_number']
        route_id = request.form.get('route_id')
        boarding_point_id = request.form.get('boarding_point_id')

        # Validate input
        if not student_name or not enrollment_number:
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('students'))

        # Check if enrollment number already exists
        existing_student = Student.query.filter_by(enrollment_number=enrollment_number).first()
        if existing_student:
            flash(f'Enrollment number {enrollment_number} already exists!', 'error')
            return redirect(url_for('students'))

        new_student = Student(
            student_name=student_name,
            enrollment_number=enrollment_number,
            route_id=route_id if route_id else None,
            boarding_point_id=boarding_point_id if boarding_point_id else None
        )
        db.session.add(new_student)

        try:
            db.session.commit()
            flash('Student added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'error')

        return redirect(url_for('students'))

    students = Student.query.all()
    routes = Route.query.all()
    return render_template('students.html', students=students, routes=routes)


@app.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')

    return redirect(url_for('students'))


@app.route('/get-boarding-points/<int:route_id>')
def get_boarding_points(route_id):
    boarding_points = BoardingPoint.query.filter_by(route_id=route_id).order_by(BoardingPoint.stop_number).all()
    return render_template('boarding_points_dropdown.html', boarding_points=boarding_points)


# Toggle dark mode
@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    if 'theme' in session and session['theme'] == 'dark':
        session['theme'] = 'light'
    else:
        session['theme'] = 'dark'
    referrer = request.referrer or url_for('index')
    return redirect(referrer)


# Import CET bus routes
@app.route('/import-cet-routes', methods=['POST'])
@login_required
def import_cet_routes():
    try:
        init_db_from_schema()
        flash("CET bus routes imported successfully!", "success")
    except Exception as e:
        flash(f"Error importing routes: {str(e)}", "error")

    return redirect(url_for('routes'))


@app.route('/auto-login',methods=['GET', 'POST'])
def auto_login():
    user = User.query.first()
    if not user:
        user = User(email="admin@college.edu", name="Admin", is_admin=True)
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('Auto-login successful!', 'success')
    return redirect(url_for('index'))


@app.route('/chatbot', methods=['GET'])
@login_required
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    try:
        import google.generativeai as genai
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBouqkJ2-hlZDXlmmuPhxDKuuqtontg_hM')
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')  # Update to a valid model name
        data = request.get_json()
        prompt = data.get('message', '')
        if not prompt:
            return {"reply": "Please enter a message."}
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        reply = f"Sorry, the AI service is currently unavailable. ({str(e)})"
    return {"reply": reply}


@app.route('/complaints', methods=['GET', 'POST'])
@login_required
def complaints():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        bus_id = request.form.get('bus_id')
        if not subject or not message:
            flash('Please fill all fields!', 'error')
            return redirect(url_for('complaints'))
        complaint = Complaint(
            user_id=current_user.id if current_user.is_authenticated else None,
            bus_id=bus_id if bus_id else None,
            subject=subject,
            message=message
        )
        db.session.add(complaint)
        try:
            db.session.commit()
            flash('Complaint submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting complaint: {str(e)}', 'error')
        return redirect(url_for('complaints'))
    buses = Bus.query.all()
    return render_template('complaints.html', buses=buses)

@app.route('/admin/complaints')
@login_required
def view_complaints():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('view_complaints.html', complaints=complaints)


if __name__ == '__main__':
    app.run(debug=True)
