import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

print("Loaded SECRET_API_KEY:", os.environ.get('SECRET_API_KEY'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

API_KEY = os.environ.get('SECRET_API_KEY', 'dev_key')
if API_KEY == 'dev_key':
    print("WARNING: Using fallback API key 'dev_key'. Ensure SECRET_API_KEY is set correctly in .env.")
app.config['SECRET_API_KEY'] = API_KEY

db = SQLAlchemy(app)

def api_key_required(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and api_key == app.config['SECRET_API_KEY']:
            return f(*args, **kwargs)
        return make_response(jsonify({'message': 'Authorization Required: Invalid or missing X-API-KEY header.'}), 401)
    decorated_function.__name__ = f.__name__
    return decorated_function

class CourseModel(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    units = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True, default="No description")
    prerequisite = db.Column(db.String(255), nullable=True, default="No requirements")
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'title': self.title,
            'instructor': self.instructor,
            'units': self.units,
            'description': self.description or "No description",
            'prerequisite': self.prerequisite or "No requirements"
        }

@app.route('/', methods=['GET'])
def documentation():
    docs = {
        "title": "Course API Documentation (v1)",
        "endpoints": [
            {"route": "/", "method": "GET", "security": "Public"},
            {"route": "/courses", "method": "GET", "security": "Public"},
            {"route": "/courses/<int:id>", "method": "GET", "security": "Public"},
            {"route": "/courses", "method": "POST", "security": "Protected"},
            {"route": "/courses/<int:id>", "method": "PATCH", "security": "Protected"},
            {"route": "/courses/<int:id>", "method": "DELETE", "security": "Protected"}
        ]
    }
    return jsonify(docs)

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = CourseModel.query.all()
    return jsonify([course.to_dict() for course in courses])

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = CourseModel.query.get(course_id)
    if not course:
        return make_response(jsonify({'message': f'Course ID {course_id} not found.'}), 404)
    return jsonify(course.to_dict())

@app.route('/courses', methods=['POST'])
@api_key_required
def create_course():
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify({'message': 'Request body must be valid JSON.'}), 400)
    
    required_fields = ['course_code', 'title', 'instructor', 'units']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({'message': f'Missing required fields: {", ".join(required_fields)}'}), 400)

    try:
        units_float = float(data['units'])
    except ValueError:
        return make_response(jsonify({'message': 'Units must be a valid number.'}), 400)
    
    try:
        new_course = CourseModel(
            course_code=data['course_code'],
            title=data['title'],
            instructor=data['instructor'],
            units=units_float,
            description=data.get('description'),
            prerequisite=data.get('prerequisite')
        )
        db.session.add(new_course)
        db.session.commit()
        return make_response(jsonify({'message': 'Course created successfully', 'course': new_course.to_dict()}), 201)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Course code already exists.'}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)

@app.route('/courses/<int:course_id>', methods=['PATCH'])
@api_key_required
def update_course(course_id):
    course = CourseModel.query.get(course_id)
    if not course:
        return make_response(jsonify({'message': f'Course ID {course_id} not found.'}), 404)

    data = request.get_json()
    if 'course_code' in data: course.course_code = data['course_code']
    if 'title' in data: course.title = data['title']
    if 'instructor' in data: course.instructor = data['instructor']
    if 'units' in data:
        try:
            course.units = float(data['units'])
        except ValueError:
            return make_response(jsonify({'message': 'Units must be a valid number.'}), 400)
    if 'description' in data: course.description = data['description']
    if 'prerequisite' in data: course.prerequisite = data['prerequisite']

    try:
        db.session.commit()
        return jsonify({'message': 'Course updated successfully', 'course': course.to_dict()})
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'message': 'Course code already exists.'}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'message': f'Internal Server Error: {str(e)}'}), 500)

@app.route('/courses/<int:course_id>', methods=['DELETE'])
@api_key_required
def delete_course(course_id):
    course = CourseModel.query.get(course_id)
    if not course:
        return make_response(jsonify({'message': f'Course ID {course_id} not found.'}), 404)
    
    db.session.delete(course)
    db.session.commit()
    return make_response(jsonify({'message': f'Course {course_id} deleted successfully'}), 204)

if __name__ == '__main__':
    app.run()
