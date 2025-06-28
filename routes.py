from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session, flash
from flask_login import login_user, logout_user, login_required, login_manager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import Student, Course, Enrollment
from forms import RegistrationForm, LoginForm
from datetime import datetime
from app import login_manager

main_bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = Student.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('main.register'))
        
        student = Student(
            name=form.name.data,
            email=form.email.data
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and student.check_password(form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).join(Course).all()
    return render_template('dashboard.html', enrollments=enrollments)

@main_bp.route('/courses')
def courses():
    return render_template('courses.html')

@main_bp.route('/api/courses')
def api_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@main_bp.route('/api/my-courses')
@login_required
def my_courses():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    courses = [Course.query.get(enrollment.course_id) for enrollment in enrollments]
    return jsonify([course.to_dict() for course in courses])

@main_bp.route('/ajax/enroll', methods=['POST'])
@login_required
def ajax_enroll():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Request must be JSON'}), 415
        
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'success': False, 'message': 'Course ID is required'}), 400
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'success': False, 'message': 'Course not found'}), 404
    
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        return jsonify({'success': False, 'message': 'Already enrolled in this course'}), 400
    
    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Enrollment successful',
        'course': course.to_dict()
    })

@main_bp.route('/ajax/unenroll/<int:course_id>', methods=['DELETE'])
@login_required
def ajax_unenroll(course_id):
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        return jsonify({'success': False, 'message': 'Enrollment not found'}), 404
    
    db.session.delete(enrollment)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Unenrollment successful'
    })

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))