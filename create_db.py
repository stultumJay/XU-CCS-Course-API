from api import app, db, CourseModel

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select

with app.app_context():
    db.create_all()