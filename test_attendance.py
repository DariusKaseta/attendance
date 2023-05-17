import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from attendance import Teacher, AttStatus, Lesson, Student, StudentAttendance
from datetime import datetime

engine = create_engine('sqlite:///attendance.db')
session = sessionmaker(bind=engine)()

class Base(DeclarativeBase):
    pass


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///attendance.db')
        session = sessionmaker(bind=self.engine)
        self.session = session()


    def tearDown(self):
        self.session.close()
        self.engine.dispose()


    def test_create_teacher(self):
        techer = Teacher(f_name="Burokas", l_name="Raudonas", subject="Matematika")
        self.session.add(techer)
        self.session.commit()

        saved_teacher = self.session.query(Teacher).filter_by(f_name="Burokas").first()
        self.assertEqual(saved_teacher.f_name, "Burokas")
        self.assertEqual(saved_teacher.l_name, "Raudonas")
        self.assertEqual(saved_teacher.subject, "Matematika")


    def test_creat_lesson(self):
        teacher = Teacher(f_name="Burokas", l_name="Raudonas", subject="Matematika")
        self.session.add(teacher)
        self.session.commit()

        expected_date = datetime.utcnow()

        lesson = Lesson(date_=expected_date, teacher=teacher)
        self.session.add(lesson)
        self.session.commit()

        saved_lesson = self.session.query(Lesson).filter_by(id=lesson.id).first()
        self.assertEqual(saved_lesson.date_, expected_date.date())
        self.assertEqual(saved_lesson.teacher_id, teacher.id)


    def test_create_student(self):
        student = Student(student_fname="Morka", student_lname="Orandzine")
        self.session.add(student)
        self.session.commit()

        saved_student = self.session.query(Student).filter_by(id=student.id).first()
        self.assertEqual(saved_student.student_fname, "Morka")
        self.assertEqual(saved_student.student_lname, "Orandzine")


    def test_AttStatus(self):
        att_status_present = AttStatus(name="Present")
        att_status_absent = AttStatus(name="Absent")
        att_status_late = AttStatus(name="Late")

        self.session.add_all([att_status_present, att_status_absent, att_status_late])
        self.session.commit()

        self.assertEqual(att_status_present.name, "Present")
        self.assertEqual(att_status_absent.name, "Absent")
        self.assertEqual(att_status_late.name, "Late")
        self.assertEqual(len(att_status_present.student_attendance), 0)
        self.assertEqual(len(att_status_absent.student_attendance), 0)
        self.assertEqual(len(att_status_late.student_attendance), 0)

        # expected_repr = "1, Present"
        # self.assertEqual(repr(att_status), expected_repr)


    def test_StudentAttendance(self):
        att_status = AttStatus(name="Present")
        student = Student(student_fname="Morka", student_lname="Orandzine")
        lesson = Lesson(date_=datetime.utcnow())

        attendance = StudentAttendance(lesson=lesson, student=student, status=att_status)

        self.session.add_all([att_status, student, lesson, attendance])
        self.session.commit()

        # self.assertEqual(attendance.lesson_id, lesson.id)
        # self.assertEqual(attendance.student_id, student.id)
        # self.assertEqual(attendance.attstatus_id, att_status.id)
        # self.assertEqual(attendance.lesson, lesson.id)
        # self.assertEqual(attendance.student, student.id)
        # self.assertEqual(attendance.status, att_status.id)

        expected_repr = f"{attendance.id}, {attendance.lesson_id}, {attendance.student_id}, {attendance.attstatus_id}"
        self.assertEqual(repr(attendance), expected_repr)


if __name__ == '__main__':
    unittest.main()