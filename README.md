# XU-CCS Course Management API (v1)

This is a simple RESTful API built using **Flask** and **SQLite** that lets you manage course information such as course codes, titles, instructors, and units. It’s designed to be lightweight and easy to understand — perfect for learning how APIs work locally without external dependencies. You can use this API to create, retrieve, update, and delete courses in your database.

---

## 🚀 Setup Instructions

### 1\. Clone the Repository
```bash
git clone [https://github.com/stultumJay/XU-CCS-Course-API.git](https://github.com/stultumJay/XU-CCS-Course-API.git)
cd XU-CCS-Course-API
````

### 2\. Create and Activate a Virtual Environment

For **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Create the Database

```bash
python create_db.py
```

### 5\. Run the API

```bash
python api.py
```

The API will now be running at:
👉 **http://127.0.0.1:5000/**

-----

## 🧪 Testing the API

You can test this API using any of the following tools:

  * **Thunder Client** (VS Code Extension)
  * **Postman**
  * **Command Prompt / Terminal** (using `curl`)

-----

## 📚 API Documentation

```json
{
    "API Title": "Course Management API (v1)",
    "Base URL": "[http://127.0.0.1:5000/](http://127.0.0.1:5000/)",
    "Description": "A RESTful API for managing course data, including creation, retrieval, updates, and deletion of course records.",
    "Endpoints": [
        {
            "Endpoint": "List All Courses",
            "Method": "GET",
            "URL": "[http://127.0.0.1:5000/courses](http://127.0.0.1:5000/courses)",
            "Parameters": {
                "None": "Returns all courses in the database."
            },
            "Example": "GET [http://127.0.0.1:5000/courses](http://127.0.0.1:5000/courses)"
        },
        {
            "Endpoint": "Retrieve Course by ID",
            "Method": "GET",
            "URL": "[http://127.0.0.1:5000/courses/](http://127.0.0.1:5000/courses/)<int:id>",
            "Parameters": {
                "id": "Integer – The ID of the course to retrieve."
            },
            "Example": "GET [http://127.0.0.1:5000/courses/1](http://127.0.0.1:5000/courses/1)"
        },
        {
            "Endpoint": "Create a New Course",
            "Method": "POST",
            "URL": "[http://127.0.0.1:5000/courses](http://127.0.0.1:5000/courses)",
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
            "URL": "[http://127.0.0.1:5000/courses/](http://127.0.0.1:5000/courses/)<int:id>",
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
            "URL": "[http://127.0.0.1:5000/courses/](http://127.0.0.1:5000/courses/)<int:id>",
            "Parameters": {
                "id": "Integer – The ID of the course to delete."
            },
            "Example": "DELETE [http://127.0.0.1:5000/courses/1](http://127.0.0.1:5000/courses/1)",
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
```

-----

## 🧩 Example Curl Commands

**List all courses:**

```bash
curl [http://127.0.0.1:5000/courses](http://127.0.0.1:5000/courses)
```

**Get a specific course:**

```bash
curl [http://127.0.0.1:5000/courses/1](http://127.0.0.1:5000/courses/1)
```

**Add a new course:**

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"course_code\":\"CS102\",\"title\":\"Data Structures\",\"instructor\":\"Prof. Jane\",\"units\":4,\"description\":\"Advanced data structures and algorithms.\",\"prerequisite\":\"CS101\"}" [http://127.0.0.1:5000/courses](http://127.0.0.1:5000/courses)
```

**Update a course:**

```bash
curl -X PATCH -H "Content-Type: application/json" -d "{\"units\":5}" [http://127.0.0.1:5000/courses/1](http://127.0.0.1:5000/courses/1)
```

**Delete a course:**

```bash
curl -X DELETE [http://127.0.0.1:5000/courses/1](http://127.0.0.1:5000/courses/1)
```

© 2025 Course Management API — Gerfel Jay Jimenez
