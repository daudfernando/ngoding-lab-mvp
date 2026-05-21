from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="student")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="user")
    submissions = relationship("Submission", back_populates="user")
    progress = relationship("StudentProgress", back_populates="user")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    level_name = Column(String(100), default="Beginner")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course", order_by="Lesson.lesson_order")
    codes = relationship("CourseCode", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(String(30), default="active")
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    lesson_order = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="lessons")
    tasks = relationship("Task", back_populates="lesson", order_by="Task.task_order")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(200), nullable=False)
    instruction = Column(Text, default="")
    task_type = Column(String(50), nullable=False)
    task_order = Column(Integer, default=1)
    expected_answer = Column(Text, default="")
    starter_code = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="tasks")
    options = relationship("TaskOption", back_populates="task", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="task", cascade="all, delete-orphan", order_by="TestCase.test_order")
    submissions = relationship("Submission", back_populates="task")


class TaskOption(Base):
    __tablename__ = "task_options"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    task = relationship("Task", back_populates="options")


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    input_data = Column(Text, default="")
    expected_output = Column(Text, default="")
    test_order = Column(Integer, default=1)

    task = relationship("Task", back_populates="test_cases")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    submitted_answer = Column(Text, default="")
    submitted_code = Column(Text, default="")
    status = Column(String(30), nullable=False)
    feedback = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    task = relationship("Task", back_populates="submissions")


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
    course = relationship("Course")
    lesson = relationship("Lesson")
    task = relationship("Task")


class CourseCode(Base):
    __tablename__ = "course_codes"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    code = Column(String(80), nullable=False, unique=True, index=True)
    max_users = Column(Integer, default=1)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expired_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="codes")
