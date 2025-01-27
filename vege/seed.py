from ipaddress import summarize_address_range
from venv import create
from faker import Faker

fake = Faker()
import random
from .models import (
    Receipe,
    StudentID,
    Student,
    Department,
    Subject,
    SubjectMarks,
    Reportcard,
)
from django.db.models import Sum
import logging
from vege.models import Department, StudentID, Student

logger = logging.getLogger(__name__)


def create_subject_marks(n):
    try:
        student_obj = Student.objects.all()
        for student in student_obj:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject, student=student, marks=random.randint(0, 100)
                )

    except Exception as e:
        print(e)


def seed_db(n=10) -> None:
    try:
        for __ in range(n):
            department_objs = Department.objects.all()
            random_index = random.randint(0, len(department_objs) - 1)
            student_id = f"STU-0{random.randint(100,999)}"
            department = department_objs[random_index]
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )

    except Exception as e:
        print(e)


def generate_report_card():
    print("Called")
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks", "-student_age"
    )
    logger.info(ranks)
    i = 1
    for rank in ranks:
        Reportcard.objects.create(student=rank, student_rank=i)
        i = i + 1
