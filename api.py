from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Landing Page of the API
@app.route('/', methods=['GET'])
def documentation():
    docs = {
        "API Title": "Course Management API (v1)",
        "Base URL": "http://127.0.0.1:5000/",
        "Description": "A RESTful API for managing course data, including creation, retrieval, updates, and deletion of course records.",
        "Endpoints": [
            {
                "Endpoint": "List All Courses",
                "Method": "GET",
                "URL": "http://127.0.0.1:5000/courses",
                "Parameters": {
                    "None": "Returns all courses in the database."
                },
                "Example": "GET http://127.0.0.1:5000/courses"
            },
            {
                "Endpoint": "Retrieve Course by ID",
                "Method": "GET",
                "URL": "http://127.0.0.1:5000/courses/<int:id>",
                "Parameters": {
                    "id": "Integer – The ID of the course to retrieve."
                },
                "Example": "GET http://127.0.0.1:5000/courses/1"
            },
            {
                "Endpoint": "Create a New Course",
                "Method": "POST",
                "URL": "http://127.0.0.1:5000/courses",
                "Parameters": {
                    "course_code": "String – Unique course code (required)",
                    "title": "String – Course title (required)",
                    "instructor": "String – Instructor name (required)",
                    "units": "Float – Number of units (required)",
                    "description": "String – Optional course description",
                    "prerequisite": "String – Optional prerequisite information"
                },
                "Example Request": {
                    "course_code": "CS101",
                    "title": "Introduction to Computer Science",
                    "instructor": "Dr. Smith",
                    "units": 3,
                    "description": "Basic programming and algorithms.",
                    "prerequisite": "None"
                },
                "Example Response": {
                    "message": "Course created successfully",
                    "course": {
                        "id": 1,
                        "course_code": "CS101",
                        "title": "Introduction to Computer Science",
                        "instructor": "Dr. Smith",
                        "units": 3,
                        "description": "Basic programming and algorithms.",
                        "prerequisite": "None"
                    }
                }
            },
            {
                "Endpoint": "Update Course",
                "Method": "PATCH",
                "URL": "http://127.0.0.1:5000/courses/<int:id>",
                "Parameters": {
                    "id": "Integer – The ID of the course to update.",
                    "course_code": "String – Updated course code (optional)",
                    "title": "String – Updated title (optional)",
                    "instructor": "String – Updated instructor (optional)",
                    "units": "Float – Updated number of units (optional)",
                    "description": "String – Updated course description (optional)",
                    "prerequisite": "String – Updated prerequisite (optional)"
                },
                "Example Request": {
                    "title": "Intro to Computing",
                    "units": 4
                },
                "Example Response": {
                    "message": "Course updated successfully",
                    "course": {
                        "id": 1,
                        "course_code": "CS101",
                        "title": "Intro to Computing",
                        "instructor": "Dr. Smith",
                        "units": 4,
                        "description": "Basic programming and algorithms.",
                        "prerequisite": "None"
                    }
                }
            },
            {
                "Endpoint": "Delete Course",
                "Method": "DELETE",
                "URL": "http://127.0.0.1:5000/courses/<int:id>",
                "Parameters": {
                    "id": "Integer – The ID of the course to delete."
                },
                "Example": "DELETE http://127.0.0.1:5000/courses/1",
                "Example Response": {
                    "message": "Course 1 deleted successfully"
                }
            }
        ],
        "Response Format": {
            "id": "Unique course ID",
            "course_code": "Course code (string)",
            "title": "Course title (string)",
            "instructor": "Instructor name (string)",
            "units": "Number of units (float)",
            "description": "Course description (string)",
            "prerequisite": "Course prerequisite (string)"
        }
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
def update_course(course_id):
    course = CourseModel.query.get(course_id)
    if not course:
        return make_response(jsonify({'message': f'Course ID {course_id} not found.'}), 404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'Request body must be valid JSON.'}), 400)

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
def delete_course(course_id):
    course = CourseModel.query.get(course_id)
    if not course:
        return make_response(jsonify({'message': f'Course ID {course_id} not found.'}), 404)
    
    db.session.delete(course)
    db.session.commit()
    return make_response(jsonify({'message': f'Course {course_id} deleted successfully'}), 204)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
