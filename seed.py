from app import create_app
from models import db, Course, Student

app = create_app()

with app.app_context():
    # Add some courses
    courses = [
        Course(title='Introduction to Python', description='Learn Python programming basics'),
        Course(title='Web Development with Flask', description='Build web applications with Flask'),
        Course(title='Database Design', description='Learn relational database concepts'),
        Course(title='JavaScript Fundamentals', description='Master JavaScript programming'),
        Course(title='Advanced Algorithms', description='Study complex algorithms and data structures')
    ]
    
    for course in courses:
        db.session.add(course)
    
    # Add a test student
    test_student = Student(
        name='Test User',
        email='test@example.com'
    )
    test_student.set_password('123qwe!@#QWE')
    db.session.add(test_student)
    
    db.session.commit()
    print("Database seeded successfully!")